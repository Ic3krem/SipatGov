import logging
from database import SessionLocal, LGU
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_new_lgus():
    """Add new LGUs to the database"""
    db = SessionLocal()
    
    try:
        new_lgus = [
            {
                "name": "City of Taguig",
                "url": "https://taguig.gov.ph",
                "contact_info": "info@taguig.gov.ph",
                "budget_endpoint": "https://taguig.gov.ph/budget"
            },
            {
                "name": "Province of Batangas",
                "url": "https://batangas.gov.ph",
                "contact_info": "info@batangas.gov.ph",
                "budget_endpoint": "https://batangas.gov.ph/budget"
            }
        ]
        
        for lgu_data in new_lgus:
            # Check if LGU already exists
            existing = db.query(LGU).filter(LGU.name == lgu_data["name"]).first()
            if existing:
                logger.info(f"{lgu_data['name']} already exists (ID: {existing.id})")
                continue
            
            lgu = LGU(
                name=lgu_data["name"],
                url=lgu_data["url"],
                contact_info=lgu_data["contact_info"],
                budget_endpoint=lgu_data["budget_endpoint"],
                created_at=datetime.utcnow()
            )
            db.add(lgu)
            db.commit()
            logger.info(f"Added {lgu_data['name']} (ID: {lgu.id})")
        
        db.close()
        logger.info("New LGUs added successfully!")
        
    except Exception as e:
        logger.error(f"Error adding LGUs: {str(e)}")
        db.close()

if __name__ == "__main__":
    add_new_lgus()
