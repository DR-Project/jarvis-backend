import asyncio
import random
import re

import nonebot
from nonebot import get_driver, require
from nonebot.config import Env
from nonebot.log import logger
from nonebot.adapters.cqhttp import Message, MessageEvent, GroupMessageEvent, Bot
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
GROUPS = [***, ***]
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
async def _queshi(bot: Bot, event: MessageEvent):
    if data_source.to_be_or_not_be(10):
        text = '确实'
        await bot.send(event, text, at_sender=False)


@diu_all.handle()
async def _diu_all(bot: Bot, event: GroupMessageEvent):
    if event.sender.role != 'member':
        msg = Message({
            'type': 'at',
            'data': {
                'qq': 'all'
            }
        })
        bot_status = await bot.get_group_member_info(group_id=event.group_id, user_id=***)
        if bot_status['role'] != 'member':
            await bot.send(event, msg, at_sender=False)
            return
    await bot.send(event, '权限不足', at_sender=False)


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

        message = Message({
            'type': 'text',
            'data': {
                'text': '抽卡小游戏已上线，发送「单抽」进行抽卡 或者「%s」查看当前群的 SSR 是谁' % 'showssr|查看SSR'
            }
        })
        logger.info('群[group_id=%d]的 SSR 已经更新，新的 SSR 是[qq=%d]' % (group, ssr_id))
        await bot.send_group_msg(group_id=group, message=message, auto_escape=True)


@lookup_ssr.handle()
async def _lookup_ssr(bot: Bot, event: GroupMessageEvent):
    if Env().environment == 'dev':
        logger.debug('当前配置环境配置为dev。跳过 lookup_ssr 功能')
        await lookup_ssr.send(Message('目前机器人所处于开发环境，不支持此功能'))
        return
    group_id = event.group_id
    ssr_id = SSR_DICT[group_id]
    ssr_info = await bot.get_group_member_info(group_id=group_id, user_id=ssr_id)

    message = Message('当前群的SSR是 @%s' % (ssr_info.get('card') if ssr_info.get('card') else ssr_info.get('nickname')))
    await lookup_ssr.finish(message)


@scheduler.scheduled_job('cron', id='roll_ssr', hour=0, minute=2)
async def update_ssr():
    if not SSR_DICT:
        return

    bot: Bot = nonebot.get_bot(str(BOT_QNUM))
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
                ret.append('\n%d. @%s 共抽卡%d次, 其中SSR %d次, 概率为%s%%' % (order, user_info.get('nickname'), total, lucky,
                                                                 '{:.2f}'.format(probability)))

            message = Message('\n'.join(ret))
            await ssr_statistics.send(message)
            SSR_STATISTICS.clear()

        members = await bot.get_group_member_list(group_id=group)
        ssr_id = random.choice(members).get('user_id')

        # update SSR
        SSR_DICT[group] = ssr_id

        message = Message({
            'type': 'text',
            'data': {
                'text': '本群今天的SSR已重置'
            }
        })
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
        await bot.send(event, '以应对风控，十连功能暂时关闭，单抽概率提升')
        return
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
        await bot.send(event, '该群人数不足', at_sender=True)
        logger.debug('群成员不足，正在退出该方法...')
        return

    # 非SSR的每个群友被抽中的概率
    weights_each_normal_member = counts_member_without_ssr / weights_all_normal_member

    weights = [weights_each_normal_member for _ in range(len(member_ids))]

    member_ids.append(ssr_id)
    weights.append(100 - weights_all_normal_member)
    # 抽取且放回
    rest_members = random.choices(member_ids, weights=weights, k=10)
    logger.info('群[group_id=%s]的[qq=%d]正在抽取十连，结果已经产生 %s' % (group_id, event.user_id, str(rest_members)))

    diu = []
    for member in rest_members:
        diu.append({
            'type': 'text',
            'data': {
                'text': '\n@%s' % ([x.get('card') if x.get('card') else x.get('nickname') for x in group_member_list if
                                    x.get('user_id') == member][0])
            }
        })

    prefix = {
        'type': 'text',
        'data': {
            'text': '你抽的十连结果是: \n'
        }
    }
    diu.insert(0, prefix)
    diu_message = Message(diu)

    # judge
    # 抽到SSR
    if ssr_id in rest_members:
        logger.info('群[group_id=%s]的[qq=%d]已成功抽取到 SSR[qq=%d]' % (group_id, event.user_id, ssr_id))
        suffix = Message([
            {
                'type': 'text',
                'data': {
                    'text': '\n\n**其中你抽到的SSR的是: '
                }
            }, {
                'type': 'at',
                'data': {
                    'qq': ssr_id
                }
            }])

        reply = Message({
            'type': 'reply',
            'date': {
                'id': event.message_id
            }
        })
        ret = reply + diu_message + suffix
        await bot.send(event, ret, at_sender=False)
        logger.info('消息已发送 %s' % str(ret))

        # 抽到SSR并且SSR是自己
        if ssr_id == event.user_id:
            extra = Message([
                {
                    'type': 'reply',
                    'data': {
                        'id': event.message_id
                    }
                }, {
                    'type': 'text',
                    'data': {
                        'text': '没想到吧！！！SSR竟然是你自己'
                    }
                }])
            message = Message(extra)
            await bot.send(event, message, at_sender=True)
            logger.info('消息已发送 %s' % str(message))
    # 没抽到SSR
    else:
        await bot.send(event, diu_message, at_sender=False)
        logger.info('消息已发送 %s' % str(diu_message))


@diuren.handle()
async def _diuren(bot: Bot, event: MessageEvent):
    msg = event.get_plaintext()
    if msg == '***':
        num = event.message_id
        at_mem = [{  # 新加的这个作为测试，没问题的话，就扩展到全部的食用性功能上面
            'type': 'reply',  # 这里改了一下，更符合逻辑。记得测试,
            # 如果不行，可能要在原来的基础上，加上这个，就是又要at type 又要reply type
            'data': {
                'id': num
            }
        }, {
            'type': 'text',
            'data': {
                'text': ' 好逊哦，丢哪个胖 '
            }
        }]
    elif msg == '***':
        at_mem = [{
            'type': 'at',
            'data': {
                'qq': data_source.mem_dicts['***']
            }
        }, {
            'type': 'text',
            'data': {
                'text': ' 丢人'
            }
        }]
    else:
        num = data_source.mem_dicts[msg[1:]]
        at_mem = Message([{
            'type': 'at',
            'data': {
                'qq': num
            }
        }, {
            'type': 'text',
            'data': {
                'text': ' 丢人 '
            }
        }])
    await bot.send(event, at_mem, at_sender=False)


@random_diuren.handle()
async def _random_diuren(bot: Bot, event: GroupMessageEvent):
    gid = event.group_id
    mem_list = await bot.get_group_member_list(group_id=gid)
    lists = []
    for i in mem_list:
        lists.append(i['user_id'])
    lists.remove(BOT_QNUM)
    luck_dog = random.sample(lists, 1)[0]
    at_mem = Message([{
        'type': 'at',
        'data': {
            'qq': luck_dog
        }
    }, {
        'type': 'text',
        'data': {
            'text': ' 丢人 '
        }
    }])
    await bot.send(event, at_mem, at_sender=False)


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

    logger.info('[qq=%d]在群[group_id=%d]已使用%d次单抽功能' % (user_id, group_id,
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

    ssr_message = Message({
        'type': 'text',
        'data': {
            'text': '@%s' % ([x.get('card') if x.get('card') else x.get('nickname') for x in group_member_list if
                              x.get('user_id') == rest_members][0])
        }
    })

    prefix = Message({
        'type': 'text',
        'data': {
            'text': '你抽的单抽结果是: '
        }
    })

    result = Message({
        'type': 'text',
        'data': {
            'text': '\n\n你没有抽到SSR哦'
        }
    })

    if ssr_id == rest_members:
        SSR_STATISTICS[group_id][user_id]['lucky'] += 1
        logger.info('[qq=%d]在群[group_id=%d]已抽到%d次SSR')

        result = Message({
            'type': 'text',
            'data': {
                'text': '\n\n你成功抽到SSR了！'
            }
        })

    reply = Message({
        'type': 'reply',
        'data': {
            'id': event.message_id
        }
    })

    message = reply + prefix + ssr_message + result
    await bot.send(event, message, at_sender=True)

    if ssr_id == event.user_id and ssr_id == rest_members:
        extra = Message({
            'type': 'text',
            'data': {
                'text': '没想到吧 SSR 竟然是你自己'
            }
        })

        ret = reply + extra
        await bot.send(event, ret, at_sender=True)


@diuren_pot.handle()
async def diuren_pot(bot: Bot, event: MessageEvent):
    at_mem = Message([{
        'type': 'at',
        'data': {
            'qq': ***
        }
    }, {
        'type': 'text',
        'data': {
            'text': ' 出来挨打 '
        }
    }])
    await bot.send(event, at_mem, at_sender=False)


@mc_diu.handle()
async def mc_diu(bot: Bot, event: MessageEvent):
    if event.get_user_id() == str(data_source.mem_dicts['***']):
        msg = Message([{
            'type': 'text',
            'data': {
                'text': '出来恰金拱门！🍟\n'
            }
        }, {
            'type': 'at',
            'data': {
                'qq': data_source.mem_dicts['***']
            }
        }, {
            'type': 'at',
            'data': {
                'qq': data_source.mem_dicts['***']
            }
        }, {
            'type': 'at',
            'data': {
                'qq': data_source.mem_dicts['***']
            }
        }])
        await bot.send(event, msg, at_sender=False)
    else:
        ret = Message([{
            'type': 'text',
            'data': {
                'text': '不许丢！🍟🍟🍟 \n'
            }
        }, {
            'type': 'at',
            'data': {
                'qq': event.get_user_id()
            }
        }])
        await bot.send(event, ret, at_sender=False)


@***_report.handle()
async def ***_report(bot: Bot, event: MessageEvent):
    msg = data_source.get_***_report()
    await bot.send(event, msg, at_sender=False)


@plus1s.handle()
async def plus1s(bot: Bot, event: MessageEvent):
    msg = '+1s'
    await bot.send(event, msg, at_sender=False)
