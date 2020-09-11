from django.test import TestCase
from model_bakery import baker

from nupe.file.models.image_upload import ProfileImage
from nupe.file.services import ImageUploadService
from nupe.resources.const.datas.image_upload import PROFILE_IMAGE_JPEG, PROFILE_IMAGE_PNG
from nupe.tests.utils import mock_image, remove_all_files_in_dir, remove_images


class ProfileImageTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        remove_images(paths=[PROFILE_IMAGE_JPEG, PROFILE_IMAGE_PNG])
        remove_all_files_in_dir()

    def test_has_all_attributes(self):
        self.assertIs(hasattr(ProfileImage, "image"), True)
        self.assertIs(hasattr(ProfileImage, "attachment_id"), True)
        self.assertIs(hasattr(ProfileImage, "public_id"), True)
        self.assertIs(hasattr(ProfileImage, "uploaded_at"), True)
        self.assertIs(hasattr(ProfileImage, "updated_at"), True)

    def test_return_str(self):
        mocked_image = mock_image()

        self.assertEqual(str(mocked_image), mocked_image.image.url)

    def test_return_properties(self):
        mocked_image = mock_image()

        self.assertEqual(mocked_image.url, mocked_image.image.url)

    def test_invalid_remove_file_service(self):
        invalid_instace = baker.make("core.Person")

        image_service = ImageUploadService()

        with self.assertRaises(ValueError):
            image_service.remove_file(instance=invalid_instace)

    def test_make_path_image_jpeg(self):
        mocked_image = mock_image(filename=PROFILE_IMAGE_JPEG)
        _, extension = mocked_image.url.rsplit(".", 1)

        self.assertEqual(extension, "jpeg")