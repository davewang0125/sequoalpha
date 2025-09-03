`from main import app, db
from models import User, Document
from datetime import datetime
import bcrypt

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Create admin user
            admin_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin_user = User(
                username='admin',
                email='admin@sequoalpha.com',
                full_name='SequoAlpha Administrator',
                hashed_password=admin_password,
                is_active=True,
                is_admin=True
            )
            db.session.add(admin_user)
            
            # Create regular user
            user_password = bcrypt.hashpw("user123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            regular_user = User(
                username='user',
                email='user@sequoalpha.com',
                full_name='Regular User',
                hashed_password=user_password,
                is_active=True,
                is_admin=False
            )
            db.session.add(regular_user)
            
            db.session.commit()
            print("✅ Default users created successfully!")
        else:
            print("ℹ️ Admin user already exists")
        
        # Check if sample documents already exist
        if Document.query.count() == 0:
            # Create sample documents
            sample_docs = [
                Document(
                    title="Q2 2025 Performance Report",
                    description="Quarterly performance review and market analysis",
                    category="Reports",
                    type="PDF",
                    filename="sample_report.pdf",
                    file_size="2.4 MB",
                    is_external=False,
                    external_url=None,
                    is_new=True,
                    created_by=admin_user.id
                ),
                Document(
                    title="Meridian Growth Fund Factsheet",
                    description="Fund overview, strategy, and key metrics",
                    category="Factsheets",
                    type="PDF",
                    filename="factsheet.pdf",
                    file_size="1.2 MB",
                    is_external=False,
                    external_url=None,
                    is_new=True,
                    created_by=admin_user.id
                ),
                Document(
                    title="Limited Partnership Agreement",
                    description="Terms and conditions of partnership",
                    category="Legal",
                    type="PDF",
                    filename="agreement.pdf",
                    file_size="3.8 MB",
                    is_external=False,
                    external_url=None,
                    is_new=False,
                    created_by=admin_user.id
                ),
                Document(
                    title="Monthly Market Commentary",
                    description="August market insights and outlook",
                    category="Reports",
                    type="LINK",
                    filename=None,
                    file_size="N/A",
                    is_external=True,
                    external_url="https://example.com/market-commentary.pdf",
                    is_new=True,
                    created_by=admin_user.id
                )
            ]
            
            for doc in sample_docs:
                db.session.add(doc)
            
            db.session.commit()
            print("✅ Sample documents created successfully!")
        else:
            print("ℹ️ Sample documents already exist")
        
        print("🎉 Database initialization completed!")

if __name__ == '__main__':
    init_database()
