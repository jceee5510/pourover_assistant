import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.coffeebean import CoffeeBean
from app.models.brew import Brew
from app.models.dial_in_session import DialInSession
from app.routes import dial_in_session as dial_in_session_routes
from app.schemas.dial_in_session import DialInSessionCreate


class DialInSessionRouteTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        dial_in_session_routes.SessionLocal = self.SessionLocal
        Base.metadata.create_all(bind=self.engine)

        self.db = self.SessionLocal()
        self.db.add(
            CoffeeBean(
                name="Test Bean",
                roaster="Test Roaster",
                origin="Test Origin",
                process="washed",
                notes="A test bean",
            )
        )
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_create_session_persists_a_new_dial_in_session(self):
        payload = DialInSessionCreate(
            coffee_bean_id=1,
            goal_type="balance",
            desired_notes="sweet and clean",
            preferred_profile="medium body",
        )

        session = dial_in_session_routes.create_session(payload, db=self.db)

        self.assertEqual(session.coffee_bean_id, 1)
        self.assertEqual(session.goal_type, "balance")
        self.assertEqual(session.desired_notes, "sweet and clean")
        self.assertEqual(session.preferred_profile, "medium body")
        self.assertEqual(session.status, "ACTIVE")

        persisted = self.db.query(dial_in_session_routes.DialInSession).filter_by(id=session.id).one()
        self.assertEqual(persisted.goal_type, "balance")

    def test_get_recommendation_returns_guidance_for_recent_brews(self):
        session = DialInSession(
            coffee_bean_id=1,
            goal_type="balance",
            desired_notes="sweet and clean",
            preferred_profile="medium body",
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        self.db.add_all([
            Brew(
                dial_in_session_id=session.id,
                dose_grams=18.0,
                water_grams=300.0,
                water_temperature=93.0,
                grinder="Baratza",
                grind_setting=6.0,
                filter_paper="Hario V60",
                brew_method="V60",
                bloom_time_seconds=45,
                total_brew_time_seconds=180,
                number_of_pours=3,
                sweetness=6,
                acidity=8,
                bitterness=7,
                body=6,
                clarity=7,
                overall_score=7,
                notes="A bit sharp",
            ),
            Brew(
                dial_in_session_id=session.id,
                dose_grams=18.0,
                water_grams=300.0,
                water_temperature=93.0,
                grinder="Baratza",
                grind_setting=5.5,
                filter_paper="Hario V60",
                brew_method="V60",
                bloom_time_seconds=40,
                total_brew_time_seconds=175,
                number_of_pours=3,
                sweetness=7,
                acidity=6,
                bitterness=8,
                body=6,
                clarity=8,
                overall_score=8,
                notes="More bitter",
            ),
        ])
        self.db.commit()

        recommendation = dial_in_session_routes.get_recommendation(session.id, db=self.db)

        self.assertEqual(recommendation.session_id, session.id)
        self.assertGreater(len(recommendation.suggested_changes), 0)
        self.assertIn("grind", recommendation.recommendation.lower())
        self.assertTrue(recommendation.explanation)


if __name__ == "__main__":
    unittest.main()
