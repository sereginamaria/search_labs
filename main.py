from yargy import Parser, rule
from yargy.pipelines import morph_pipeline
from yargy.interpretation import fact
from yargy.relations import gnc_relation
from yargy.predicates import gram, normalized, type

#Первые две главы книги "Коты Воители"
with open('cats_warriors.txt', encoding='UTF-8') as f:
    text = f.read()


gnc = gnc_relation()


# Правило 1. Ищет названя племен

CLAN_NAME = morph_pipeline([
    'грозовое',
    'звездное',
    'речное',
    'сумрачное'
])

Clan = fact('ClanName', ['name'])

CLAN = rule(
    CLAN_NAME.interpretation(Clan.name).match(gnc),
    normalized('племя'),
).interpretation(Clan)

print('Правило 1')
parser = Parser(CLAN)
for match in parser.findall(text):
    print([x.value for x in match.tokens])

# Правило 2. Ищет описание кошек (какая кошка)
Cat = fact('Cat', ['adjective'])


ADJECTIVE = gram('ADJF')

CAT_RULE = rule(
    ADJECTIVE.interpretation(Cat.adjective).match(gnc),
    normalized('кошка'),
).interpretation(Cat)

print('Правило 2')
parser = Parser(CAT_RULE)
for match in parser.findall(text):
    print([x.value for x in match.tokens])

# Правило 3. Ищет кто и что сделал
CatAction = fact(
    'CatAction',
    ['name', 'action']
)


NAME = gram('Name')
ACTION = gram('VERB')

NAME_PIPELINE = morph_pipeline([
    'Рыжик',
    'Синяя Звезда',
    'Коготь'
])

PERSON_ACTION_RULE = rule(
    NAME_PIPELINE.interpretation(CatAction.name).match(gnc),
    ACTION.interpretation(CatAction.action.normalized())
).interpretation(CatAction)

print('Правило 3')
parser = Parser(PERSON_ACTION_RULE)
for match in parser.findall(text):
    print([x.value for x in match.tokens])
