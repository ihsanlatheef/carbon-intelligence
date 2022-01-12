from techtest.models.article import Article
from techtest.models.region import Region
from techtest.models.author import Author 
from techtest.connector import engine, BaseModel, db_session

BaseModel.metadata.create_all(engine)

with db_session() as session:
    au = Region(code='AU', name='Australia')
    uk = Region(code='UK', name='United Kingdom')
    us = Region(code='US', name='United States of America')

    jb = Author(first_name='Joe', last_name='Bloggs')
    js = Author(first_name='John', last_name='Smith')

    session.add_all([
        au,
        uk,
        us,
        jb,
        js,
        Article(
            title='Post 1',
            content='This is a post body',
            regions=[au, uk],
            author=js
        ),
        Article(
            title='Post 2',
            content='This is the second post body',
            regions=[au, us],
            author=jb
        )
    ])
