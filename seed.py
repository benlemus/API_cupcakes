from app import app
from models import db, Cupcake

with app.app_context():
    db.drop_all()
    db.create_all()

    c1 = Cupcake(
        flavor="chocolate",
        size="large",
        rating=5,
    )

    c2 = Cupcake(
        flavor="chocolate",
        size="small",
        rating=9,
        image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
    )

    c3 = Cupcake(
        flavor='vanilla',
        size='large',
        rating=9,
        image='https://sugargeekshow.com/wp-content/uploads/2022/08/vanilla_cupcake_featured_blog.jpg'
    )

    c4 = Cupcake(
        flavor='rasberry',
        size='small',
        rating=8,
        image='https://j6e2i8c9.delivery.rocketcdn.me/wp-content/uploads/2015/07/Eggless-vanilla-cupcakes-1.jpg'
    )

    c5 = Cupcake(
        flavor='vanilla',
        size='medium',
        rating=5,
        image='https://www.mybakingaddiction.com/wp-content/uploads/2011/07/unwrapped-vanilla-cupcake-700x1050.jpg'
    )

    c6 = Cupcake(
        flavor='strawberry',
        size='small',
        rating=7,
        image='https://www.kyleecooks.com/wp-content/uploads/2020/07/Vanilla-Cupcakes-Strawberry-Buttercream-43.jpg'
    )

    c7 = Cupcake(
        flavor='cherry',
        size='xtra small',
        rating=3,
        image='https://thefrozenbiscuit.com/wp-content/uploads/2020/03/Cherry-Cupcake.jpg'
    )
    
    db.session.add_all([c1, c2, c3, c4, c5, c6, c7])
    db.session.commit()