from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

with app.app_context():
    db.drop_all()
    db.create_all()

    class CupcakeViewsTestCase(TestCase):
        """Tests for views of API."""

        def setUp(self):
            """Make demo data."""
            with app.app_context():
                Cupcake.query.delete()
                cupcake = Cupcake(**CUPCAKE_DATA)
                db.session.add(cupcake)
                db.session.commit()

                self.cupcake = cupcake
                self.id = cupcake.id
                self.flavor = cupcake.flavor
                self.size = cupcake.size
                self.rating = cupcake.rating
                self.image = cupcake.image

        def tearDown(self):
            """Clean up fouled transactions."""
            with app.app_context():
                db.session.rollback()

        def test_get_cupcakes(self):
            with app.test_client() as client:
                resp = client.get("/api/cupcakes")

                self.assertEqual(resp.status_code, 200)

                data = resp.json
                self.assertEqual(data, {
                    "cupcakes": [
                        {
                            "id": self.cupcake.id,
                            "flavor": "TestFlavor",
                            "size": "TestSize",
                            "rating": 5,
                            "image": "http://test.com/cupcake.jpg"
                        }
                    ]
                })

        def test_cupcake_details(self):

            with app.test_client() as client:
                url = f"/api/cupcakes/{self.cupcake.id}"
                resp = client.get(url)

                self.assertEqual(resp.status_code, 200)
                data = resp.json
                self.assertEqual(data, {
                    "cupcake": {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                })

        def test_cupcake_details_404(self):
            with app.test_client() as client:
                resp = client.get('/api/cupcakes/aaa')

                self.assertEqual(resp.status_code, 404)

        def test_add_cupcake(self):
            with app.test_client() as client:
                url = "/api/cupcakes"
                resp = client.post(url, json=CUPCAKE_DATA_2)

                self.assertEqual(resp.status_code, 201)

                data = resp.json

                # don't know what ID we'll get, make sure it's an int & normalize
                self.assertIsInstance(data['cupcake']['id'], int)
                del data['cupcake']['id']

                self.assertEqual(data, {
                    "cupcake": {
                        "flavor": "TestFlavor2",
                        "size": "TestSize2",
                        "rating": 10,
                        "image": "http://test.com/cupcake2.jpg"
                    }
                })

                self.assertEqual(Cupcake.query.count(), 2)

        def test_update_cupcake(self):
            with app.test_client() as client:
                url = f'/api/cupcakes/{self.cupcake.id}'
                resp = client.patch(url, json={
                    'id': self.id,
                    'flavor': self.flavor,
                    'size': 'TestSizePatch',
                    'rating': self.rating,
                    'image': self.image
                })

                data = resp.json

                self.assertIsInstance(data['cupcake']['id'], int)
                del data['cupcake']['id']

                self.assertEqual(data, {
                    "cupcake": {
                        "flavor": "TestFlavor",
                        "size": "TestSizePatch",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                })

        def test_update_cupcake_404(self):
            with app.test_client() as client:
                url = f'/api/cupcakes/aaa'
                resp = client.patch(url, json={
                    'id': self.id,
                    'flavor': self.flavor,
                    'size': 'TestSizePatch',
                    'rating': self.rating,
                    'image': self.image
                })

                self.assertEqual(resp.status_code, 404)



        def test_delete_cupcake(self):
            with app.test_client() as client:
                resp = client.delete(f'/api/cupcakes/{self.id}')

                data = resp.json

                self.assertEqual(data, {
                    'message': 'deleted'
                })

        def test_delete_cupcake_404(self):
            with app.test_client() as client:
                resp = client.delete(f'/api/cupcakes/aaa')

                self.assertEqual(resp.status_code, 404)
