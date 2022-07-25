import django_tables2 as tables

class SectionScoreTable(tables.Table):
    student = tables.Column(attrs={"td": {"style": "padding-right: 25px"}})
    score = tables.Column()