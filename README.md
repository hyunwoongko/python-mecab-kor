# python-mecab-kor
<a href="https://github.com/hyunwoongko/python-mecab-kor/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/hyunwoongko/python-mecab-kor.svg" /></a>
<a href="https://github.com/hyunwoongko/python-mecab-kor/issues"><img alt="Issues" src="https://img.shields.io/github/issues/hyunwoongko/python-mecab-kor"/></a>

## 1. Why another package? 
[python-mecab-ko](https://github.com/jonghwanhyeon/python-mecab-ko) is great package but sadly it is not being maintained well now.
So I decided to maintain it myself and I've fixed a lot of problems about installation.
Be careful that the package name is changed `ko` to `kor` because I can't keep the package name same with the original.

## 2. What OS have you tested successfully so far?
It has been successfully installed on the following OS list.
If the installation succeeds or fails on your OS, please report it through the [issue page](https://github.com/hyunwoongko/python-mecab-kor/issues). 
I will do my best to fix your errors. 

- Linux Ubuntu
- Linux CentOS
- Amazon Linux
- Mac OS

**Please note that I don't have any plan with Windows OS.**

## 3. Installation
```
pip install python-mecab-kor
```

## 4. Usage

```python
from mecab import MeCab

mecab = MeCab()

mecab.morphs('영등포구청역에 있는 맛집 좀 알려주세요.')
# ['영등포구청역', '에', '있', '는', '맛집', '좀', '알려', '주', '세요', '.']

# drop_space=False
mecab.morphs('영등포구청역에 있는 맛집 좀 알려주세요.', drop_space=False)
# ['영등포구청역', '에', ' ', '있', '는', ' ', '맛집', ' ', '좀', ' ', '알려', '주', '세요', '.']

mecab.nouns('우리나라에는 무릎 치료를 잘하는 정형외과가 없는가!')
# ['우리', '나라', '무릎', '치료', '정형외과']

mecab.pos('자연주의 쇼핑몰은 어떤 곳인가?')
# [('자연주의', 'NNG'), ('쇼핑몰', 'NNG'), ('은', 'JX'), ('어떤', 'MM'), ('곳', 'NNG'), ('인가', 'VCP+EF'), ('?', 'SF')]

# drop_space=False
mecab.pos('자연주의 쇼핑몰은 어떤 곳인가?', drop_space=False)
# [('자연주의', 'NNG'), (' ', 'SP'), ('쇼핑몰', 'NNG'), ('은', 'JX'), (' ', 'SP'), ('어떤', 'MM'), (' ', 'SP'), ('곳', 'NNG'), ('인가', 'VCP+EF'), ('?', 'SF')]

mecab.parse('즐거운 하루\n보내세요!')
# [
#     ('즐거운', Feature(
#         pos='VA+ETM', semantic=None, has_jongseong=True, reading='즐거운',
#         type='Inflect', start_pos='VA', end_pos='ETM',
#         expression='즐겁/VA/*+ᆫ/ETM/*')),
#     ('하루', Feature(
#         pos='NNG', semantic=None, has_jongseong=False, reading='하루',
#         type=None, start_pos=None, end_pos=None,
#         expression=None)),
#     ('보내', Feature(
#         pos='VV', semantic=None, has_jongseong=False, reading='보내',
#         type=None, start_pos=None, end_pos=None,
#         expression=None)),
#     ('세요', Feature(
#         pos='EP+EF', semantic=None, has_jongseong=False, reading='세요',
#         type='Inflect', start_pos='EP', end_pos='EF',
#         expression='시/EP/*+어요/EF/*')),
#     ('!', Feature(
#         pos='SF', semantic=None, has_jongseong=None, reading=None,
#         type=None, start_pos=None, end_pos=None,
#         expression=None))
# ]

# drop_space=False
mecab.parse('즐거운 하루\n보내세요!', drop_space=False)
# [
#     ('즐거운', Feature(
#         pos='VA+ETM', semantic=None, has_jongseong=True, reading='즐거운',
#         type='Inflect', start_pos='VA', end_pos='ETM',
#         expression='즐겁/VA/*+ᆫ/ETM/*')),
#     (' ', Feature(
#         pos='SP', semantic=None, has_jongseong=None, reading=None,
#         type=None, start_pos=None, end_pos=None,
#         expression=None)),
#     ('하루', Feature(
#         pos='NNG', semantic=None, has_jongseong=False, reading='하루',
#         type=None, start_pos=None, end_pos=None,
#         expression=None)),
#     ('\n', Feature(
#         pos='SP', semantic=None, has_jongseong=None, reading=None,
#         type=None, start_pos=None, end_pos=None,
#         expression=None)),
#     ('보내', Feature(
#         pos='VV', semantic=None, has_jongseong=False, reading='보내',
#         type=None, start_pos=None, end_pos=None,
#         expression=None)),
#     ('세요', Feature(
#         pos='EP+EF', semantic=None, has_jongseong=False, reading='세요',
#         type='Inflect', start_pos='EP', end_pos='EF',
#         expression='시/EP/*+어요/EF/*')),
#     ('!', Feature(
#         pos='SF', semantic=None, has_jongseong=None, reading=None,
#         type=None, start_pos=None, end_pos=None,
#         expression=None))
# ]

```

## 5. References
- [konlpy](https://github.com/konlpy/konlpy/)
- [python-mecab-ko](https://github.com/jonghwanhyeon/python-mecab-ko)
