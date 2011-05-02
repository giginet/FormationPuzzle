# -*- coding: utf-8 -*-
#
#    Created on 2011/02/20
#    Created by giginet
#
u"""
    各ユニットのパラメータ
        hp:        耐久力
        attack:    攻撃力
        limit:     行動回数限界
        frequency: 行動頻度（1フレーム）
        image:     画像ファイルパス
"""
ATTACK = {
          'hp':10,
          'attack':10,
          'limit':10,     
          'frequency':10,
          'width':60,
          'height':60,
          'image':u'../resources/image/main/unit/attack.png',
          'effect':{'enable':True,
                    'appear':'../resources/effect/attack_appear.png',
                    'disappear':None,
                    'offset':(162, 162),
                    'width':384,
                    'height':384,
                    'frame':40
            },
          'delay':35
}
GUARD = {
          'hp':30,
          'attack':4,
          'limit':10,     
          'frequency':30,
          'width':80,
          'height':20,
          'image':u'../resources/image/main/unit/guard.png',
          'effect':{'enable':True,
                    'appear':'../resources/effect/guard_appear.png',
                    'disappear':None,
                    'offset':(10,40),
                    'width':100,
                    'height':100,
                    'frame':80
            },
          'delay':60
}
SWEEP = {
          'hp':1,
          'attack':1,
          'limit':32,     
          'frequency':5,
          'width':60,
          'height':60,
          'image':u'../resources/image/main/unit/sweep.png',
          'effect':{'enable':True,
                    'appear':'../resources/effect/sweep_appear.png',
                    'disappear':None,
                    'offset':(34,34),
                    'width':128,
                    'height':128,
                    'frame':40
            },
          'delay':20
}
BOMB = {
          'hp':10,
          'attack':1,
          'limit':0,     
          'frequency':60,
          'width':40,
          'height':40,
          'image':u'../resources/image/main/unit/bomb.png',
          'effect':{'enable':True,
                    'appear':'../resources/effect/bomb_appear.png',
                    'disappear':None,
                    'offset':(12,12),
                    'width':64,
                    'height':64,
                    'frame':80
            },
          'delay':60
}