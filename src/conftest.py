import boto3
import pytest
from moto import mock_aws
from pytest_factoryboy import register

from users.factories import UserFactory
from core.factories import LanguageFactory
from movies.factories import MovieFactory, DirectorFactory, GenreFactory
from theaters.factories import TheaterHallFactory, SeatFactory
from showings.factories import ShowingFactory, ShowingFormatFactory, ShowingVariantFactory

register(ShowingFactory)
register(ShowingFormatFactory)
register(ShowingVariantFactory)
register(UserFactory)
register(LanguageFactory)
register(MovieFactory)
register(DirectorFactory)
register(GenreFactory)
register(TheaterHallFactory)
register(SeatFactory)

@pytest.fixture(autouse=True)
def mock_aws_s3(settings):
    settings.AWS_ACCESS_KEY_ID = "testing"
    settings.AWS_SECRET_ACCESS_KEY = "testing"
    settings.AWS_STORAGE_BUCKET_NAME = "test-bucket"
    settings.AWS_S3_REGION_NAME = "us-east-1"
    
    with mock_aws():
        s3 = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)
        s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        yield
