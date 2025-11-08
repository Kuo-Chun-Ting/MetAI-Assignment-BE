from urllib.parse import quote_plus

DB_HOST = "aws-1-ap-southeast-2.pooler.supabase.com"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres.cqikyhluoceusmmdokwf"
DB_PASSWORD = "1qaz@WSX3edc$RFV"


def get_database_url() -> str:
    encoded_password = quote_plus(DB_PASSWORD)
    return f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
