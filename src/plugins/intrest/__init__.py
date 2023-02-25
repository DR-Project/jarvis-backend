import asyncio
import json
import random
import re

import nonebot
from nonebot import get_driver, require
from nonebot.config import Env
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message, MessageEvent, GroupMessageEvent, Bot, MessageSegment
from nonebot.plugin import on_regex

from . import data_source
from .config import Config
from .data import SSR_DICT, SSR_STATISTICS

global_config = get_driver().config
config = Config(**global_config.dict())
scheduler = require('nonebot_plugin_apscheduler').scheduler
driver = nonebot.get_driver()

# Constant List

BOT_QNUM = ***
GROUPS = [***, ***, ***]
TEN_GACHA_SWITCH = False
SSR_ODDS = 1  # percent '1' means 1%
REG_QUESHI = '(确实|qs|有一说一|yysy|么|吗|呢|？)'
REG_DIUREN = '***'
REG_RDIUREN = '^(丢人|diuren|diu)$'
REG_PLUS1S = '.*(蛤|蛤蛤|黑框眼镜|江|泽).*'
REG_***_REPORT = '^(***排行|***ph|kk***)$'
REG_POT = '***'
REG_DIU_ALL = '^(全体丢人|全员丢人|丢全部)$'
REG_TEN_GACHA = '^(十连丢人|十连单抽|十连|十连抽)$'
REG_GACHA = '^(单抽)$'
REG_GACHA_STATISTICS = '^(gachadata|抽奖统计)$'
REG_SSR_LOOKUP = '^(showssr|查看SSR)$'
MC_DIU = '^(丢羊毛|有羊毛了|丢m记)$'

# Register Event

queshi = on_regex(REG_QUESHI)
random_diuren = on_regex(REG_RDIUREN)
diuren = on_regex(REG_DIUREN, re.IGNORECASE)
plus1s = on_regex(REG_PLUS1S)
***_report = on_regex(REG_***_REPORT, re.IGNORECASE)
diuren_pot = on_regex(REG_POT)
mc_diu = on_regex(MC_DIU, re.IGNORECASE)
diu_all = on_regex(REG_DIU_ALL)
ten_times_diu = on_regex(REG_TEN_GACHA)
single_diu = on_regex(REG_GACHA)
lookup_ssr = on_regex(REG_SSR_LOOKUP, re.IGNORECASE)
ssr_statistics = on_regex(REG_GACHA_STATISTICS, re.IGNORECASE)

''' >>>>>> Just for fun <<<<<< '''


@queshi.handle()
async def _queshi(bot: Bot, event: GroupMessageEvent):
    if data_source.to_be_or_not_be(10):
        logger.info('成功击中')
        await queshi.finish('确实')
    logger.info('没有击中')


@diu_all.handle()
async def _diu_all(bot: Bot, event: GroupMessageEvent):
    if event.sender.role != 'member':
        msg = MessageSegment.at('all')
        bot_status = await bot.get_group_member_info(group_id=event.group_id, user_id=global_config.bot_qq,
                                                     no_cache=True)
        if bot_status['role'] != 'member':  # 不是member，说明是管理员或者群主
            await diu_all.finish(msg)
    await diu_all.finish('权限不足')


@driver.on_bot_connect
async def _roll_ssr(bot: Bot):
    if Env().environment == 'dev':
        logger.debug('当前配置环境配置为dev。跳过 roll_ssr 功能')
        return
    for group in GROUPS:
        members = await bot.get_group_member_list(group_id=group)
        ssr_id = random.choice(members).get('user_id')

        # generating SSR
        SSR_DICT[group] = ssr_id

        message = '抽卡小游戏已上线，发送「单抽」进行抽卡 或者「%s」查看当前群的 SSR 是谁' % 'showssr|查看SSR'

        logger.info('群[group_id=%d]的 SSR 已经更新，新的 SSR 是[qq=%d]' % (group, ssr_id))
        await bot.send_group_msg(group_id=group, message=message, auto_escape=True)


@lookup_ssr.handle()
async def _lookup_ssr(bot: Bot, event: GroupMessageEvent):
    if Env().environment == 'dev':
        logger.debug('当前配置环境配置为dev。跳过 lookup_ssr 功能')
        await lookup_ssr.finish('目前机器人所处于开发环境，不支持此功能')
        return
    group_id = event.group_id
    ssr_id = SSR_DICT[group_id]
    ssr_info = await bot.get_group_member_info(group_id=group_id, user_id=ssr_id)

    message = '当前群的SSR是 @%s' % (ssr_info.get('card') if ssr_info.get('card') else ssr_info.get('nickname'))
    await lookup_ssr.finish(message)


@scheduler.scheduled_job('cron', id='roll_ssr', hour=0, minute=2)
async def update_ssr():
    if not SSR_DICT:
        return

    bot: Bot = nonebot.get_bot()
    for group in SSR_DICT.keys():

        # 如果一整天都没有人使用过抽卡功能，则不发送此统计
        if SSR_STATISTICS:

            group_data: dict = SSR_STATISTICS.get(group)
            logger.debug(group_data)

            ret = ['当前群的抽奖统计：']
            order = 1

            sorted_group_data = sorted(group_data.items(), key=lambda x: x[1]['total'])
            for user_data in sorted_group_data:
                total, lucky = user_data[1].get('total'), user_data[1].get('lucky')
                probability = lucky / total * 100 if lucky else 0
                user_info = await bot.get_group_member_info(group_id=group, user_id=user_data[0])
                ret.append(
                    '\n%d. @%s 共抽卡%d次, 其中SSR %d次, 概率为%s%%' % (order, user_info.get('nickname'), total, lucky,
                                                                        '{:.2f}'.format(probability)))

            message = Message('\n'.join(ret))
            await bot.send_group_msg(group_id=group, message=message, auto_escape=True)
            SSR_STATISTICS.clear()
            logger.info('今天的统计结果是： %s' % json.dumps(SSR_STATISTICS))

        members = await bot.get_group_member_list(group_id=group)
        ssr_id = random.choice(members).get('user_id')

        # update SSR
        SSR_DICT[group] = ssr_id

        message = '本群今天的SSR已重置'
        logger.info('群[group_id=%d]的SSR已经更新，新的SSR是[qq=%d]' % (group, ssr_id))
        await bot.send_group_msg(group_id=group, message=message, auto_escape=True)
        await asyncio.sleep(random.choice([i for i in range(30, 60)]))


@ssr_statistics.handle()
async def _ssr_statistics(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    group_data: dict = SSR_STATISTICS.get(group_id)
    logger.debug(group_data)

    # 还没有人使用SSR 功能
    if not group_data:
        await ssr_statistics.send('自机器人上线以来，还没有人进行过抽奖。')
        return

    ret = ['当前群组的抽奖统计：']
    order = 1

    sorted_group_data = sorted(group_data.items(), key=lambda x: x[1]['lucky'] / x[1]['total'], reverse=True)

    for user_data in sorted_group_data:
        total, lucky = user_data[1].get('total'), user_data[1].get('lucky')
        probability = lucky / total * 100 if lucky else 0
        user_info = await bot.get_group_member_info(group_id=group_id, user_id=user_data[0])
        ret.append('\n%d. @%s 共抽卡%d次, 其中SSR %d次, 概率为%s%%' % (order, user_info.get('nickname'), total, lucky,
                                                                       '{:.2f}'.format(probability)))
        order += 1

    ret_message = '\n'.join(ret)
    logger.debug(ret_message)
    message = Message(ret_message)
    await ssr_statistics.send(message)


@ten_times_diu.handle()
async def _diu_ten(bot: Bot, event: GroupMessageEvent):
    if not TEN_GACHA_SWITCH:
        await ten_times_diu.finish('以应对风控，十连功能暂时关闭，单抽概率提升')

    # SSR概率 为 100 - weights_all_normal_member
    weights_all_normal_member = 100 - SSR_ODDS
    group_id = event.group_id
    logger.info('群[group_id=%d] 开始进行十连丢人，SSR的概率是 %f ' % (group_id, 100 - weights_all_normal_member) + '%')
    group_member_list = await bot.get_group_member_list(group_id=group_id)
    ssr_id = SSR_DICT.get(group_id)
    # 获取非SSR群友QQ号
    member_ids = [x.get('user_id') for x in group_member_list if x.get('user_id') != ssr_id]
    # 非SSR群友个数
    counts_member_without_ssr = len(member_ids)

    # 群成员少于11个不能玩
    if not counts_member_without_ssr >= 10:
        logger.debug('群成员不足，正在退出该方法...')
        await ten_times_diu.finish('该群人数不足', at_sender=True)

    # 非SSR的每个群友被抽中的概率
    weights_each_normal_member = counts_member_without_ssr / weights_all_normal_member

    weights = [weights_each_normal_member for _ in range(len(member_ids))]

    member_ids.append(ssr_id)
    weights.append(100 - weights_all_normal_member)
    # 抽取且放回
    rest_members = random.choices(member_ids, weights=weights, k=10)
    logger.info('群[group_id=%s]的[qq=%d]正在抽取十连，结果已经产生 %s' % (group_id, event.user_id, str(rest_members)))

    diu = Message()
    for member in rest_members:
        diu.append('\n@%s' % ([x.get('card') if x.get('card') else x.get('nickname') for x in group_member_list if
                               x.get('user_id') == member][0]))

    prefix = '你抽的十连结果是: \n'

    diu.insert(0, prefix)

    # judge
    # 抽到SSR
    if ssr_id in rest_members:
        logger.info('群[group_id=%s]的[qq=%d]已成功抽取到 SSR[qq=%d]' % (group_id, event.user_id, ssr_id))
        suffix = Message(['\n\n**其中你抽到的SSR的是: ', MessageSegment.at(ssr_id)])

        ret = diu + suffix
        await ten_times_diu.send(ret, reply_message=True)
        logger.info('消息已发送 %s' % str(ret))

        # 抽到SSR并且SSR是自己
        if ssr_id == event.user_id:
            extra = '没想到吧！！！SSR竟然是你自己'

            await ten_times_diu.finish(extra, reply_message=True)
            logger.info('消息已发送 %s' % str(extra))
    # 没抽到SSR
    else:
        await ten_times_diu.finish(diu)
        logger.info('消息已发送 %s' % str(diu))


@diuren.handle()
async def _diuren(bot: Bot, event: GroupMessageEvent):
    msg = event.get_plaintext()
    if msg == '***':
        await diuren.finish(' 好逊哦，丢哪个胖 ', reply_message=True)

    if msg == '***':
        await diuren.finish(Message([MessageSegment.at(data_source.mem_dicts['***']), ' 丢人']))

    # 从 mem_dicts 中选取
    num = data_source.mem_dicts[msg[1:]]
    await diuren.finish(Message([MessageSegment.at(num), ' 丢人 ']))


@random_diuren.handle()
async def _random_diuren(bot: Bot, event: GroupMessageEvent):
    gid = event.group_id
    mem_list = await bot.get_group_member_list(group_id=gid)
    lists = []
    for i in mem_list:
        lists.append(i['user_id'])
    lists.remove(BOT_QNUM)
    luck_dog = random.sample(lists, 1)[0]
    at_mem = Message([MessageSegment.at(luck_dog), ' 丢人 '])

    await random_diuren.finish(at_mem)


@single_diu.handle()
async def _single_diu(bot: Bot, event: GroupMessageEvent):
    weights_all_normal_member = 100 - SSR_ODDS
    group_id = event.group_id
    user_id = event.user_id

    # 机器人重启后第一次使用 或 每日重置后第一次使用 即字典中没有当前群
    if group_id not in SSR_STATISTICS.keys():
        total = {
            'id': user_id,
            'total': 1,
            'lucky': 0
        }

        logger.info('群[group_id=%d]的[qq=%d]的中奖次数已经初始化为0' % (group_id, user_id))

        SSR_STATISTICS[group_id] = {
            user_id: total
        }

    # 非第一次使用 字典中有群员
    else:
        group_data: dict = SSR_STATISTICS[group_id]

        # 该群在机器人重新上线后并非第一次使用抽奖，但是该群的用户 user_id 是第一次使用
        if user_id not in group_data.keys():
            group_data[user_id] = {
                'id': user_id,
                'total': 1,
                'lucky': 0
            }
            logger.info('群[group_id=%d]的[qq=%d]的中奖次数已经初始化为0' % (group_id, user_id))

        # 该群的该成员不是第一次使用次功能 即字典中已经有该群员的数据了 即可以获取 total 字段直接自加
        else:
            group_data[user_id]['total'] += 1

        SSR_STATISTICS[group_id] = group_data

    logger.info('[qq=%d]在群[group_id=%d]已使用%d次抽奖功能' % (user_id, group_id,
                                                                SSR_STATISTICS[group_id][user_id]['total']))

    logger.info('群[group_id=%d] 开始进行十连丢人，SSR的概率是 %f ' % (group_id, 100 - weights_all_normal_member) + '%')
    group_member_list = await bot.get_group_member_list(group_id=group_id)
    ssr_id = SSR_DICT.get(group_id)
    member_ids = [x.get('user_id') for x in group_member_list if x.get('user_id') != ssr_id]

    counts_member_without_ssr = len(member_ids)
    weights_each_normal_member = counts_member_without_ssr / weights_all_normal_member
    weights = [weights_each_normal_member for _ in range(len(member_ids))]

    member_ids.append(ssr_id)
    weights.append(100 - weights_all_normal_member)
    rest_members = random.choices(member_ids, weights=weights)[0]
    logger.info('群[group_id=%s]的[qq=%d]正在单抽，结果已经产生 %s' % (group_id, event.user_id, rest_members))

    ssr_message = '@%s' % ([x.get('card') if x.get('card') else x.get('nickname') for x in group_member_list if
                            x.get('user_id') == rest_members][0])

    prefix = '你抽的单抽结果是: '

    result = '\n\n你没有抽到SSR哦'

    if ssr_id == rest_members:
        SSR_STATISTICS[group_id][user_id]['lucky'] += 1
        logger.info('[qq=%d]在群[group_id=%d]已抽到%d次SSR' % (user_id, group_id, SSR_STATISTICS[group_id][user_id]['lucky']))

        result = '\n\n你成功抽到SSR了！'

    message = prefix + ssr_message + result
    await single_diu.send(message, at_sender=True)

    if ssr_id == event.user_id and ssr_id == rest_members:
        await single_diu.finish('没想到吧 SSR 竟然是你自己', reply_message=True)


@diuren_pot.handle()
async def diuren_pot(bot: Bot, event: GroupMessageEvent):
    if event.group_id in (***, ***):
        await diuren_pot.finish(Message([MessageSegment.at(data_source.mem_dicts.get('***')), ' 出来挨打 ']))


@mc_diu.handle()
async def mc_diu(bot: Bot, event: GroupMessageEvent):
    # 不是目标群
    if event.group_id != ***:
        mc_diu.destroy()

    # 是***
    if event.user_id == data_source.mem_dicts['***']:
        msg = Message(['出来恰金拱门！🍟\n', MessageSegment.at(data_source.mem_dicts['***']),
                       MessageSegment.at(data_source.mem_dicts['***']), MessageSegment.at(data_source.mem_dicts['***'])])
        await mc_diu.finish(msg)

    # 不是***
    if event.user_id != data_source.mem_dicts['***']:
        await mc_diu.finish(Message(['不许丢！🍟🍟🍟 \n', MessageSegment.at(event.user_id)]))


@***_report.handle()
async def ***_report(bot: Bot, event: GroupMessageEvent):
    msg = data_source.get_***_report()
    await ***_report.finish(msg)


@plus1s.handle()
async def plus1s(bot: Bot, event: MessageEvent):
    msg = '+1s'
    await plus1s.finish(msg)
