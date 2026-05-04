from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile
from django.urls import reverse
# Create your tests here.
class ProfileModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.profile = self.user.profile

    def test_profile_creation_on_user_save(self):
        """Test that Profile is automatically created when User is created"""
        self.assertIsInstance(self.profile, Profile)
        self.assertEqual(self.profile.user, self.user)

    def test_role_default_value(self):
        """Test that role defaults to 'student'"""
        self.assertEqual(self.profile.role, "student")

    def test_role_choices(self):
        """Test that role can be set to professor"""
        self.profile.role = "professor"
        self.profile.save()
        self.assertEqual(self.profile.role, "professor")

    def test_str_method(self):
        """Test the __str__ method returns expected format"""
        expected_str = f"{self.user.username} - {self.profile.role}"
        self.assertEqual(str(self.profile), expected_str)

    def test_get_pinned_count_with_no_pinned_resources(self):
        """Test get_pinned_count returns 0 when no pinned resources exist"""
        # Assuming you have a pinned_resources ForeignKey/ManyToManyField
        count = self.profile.get_pinned_count()
        self.assertEqual(count, 0)

    def test_get_pinned_count_with_pinned_resources(self):
        """Test get_pinned_count returns correct count when pinned resources exist"""
        # You'll need to create test pinned resources
        # This depends on your Resource model - adjust accordingly
        # from your_app_name.models import Resource
        # Resource.objects.create(pinned_by=self.profile, ...)
        # Then verify the count
        pass  # Implement based on your Resource model


class UserProfileSignalTest(TestCase):
    def setUp(self):
        """Set up test data - THIS MUST BE CALLED BEFORE EACH TEST"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        # Access the profile to ensure it exists
        self.profile = self.user.profile

    def test_profile_created_after_user_creation(self):
        """Test that Profile is created via signal after User is created"""
        new_user = User.objects.create_user(
            username="newuser",
            password="pass123"
        )
        self.assertTrue(hasattr(new_user, "profile"))
        self.assertIsInstance(new_user.profile, Profile)

    def test_profile_saved_on_user_save(self):
        """Test that profile is saved when user is saved"""
        # Now self.user exists because setUp() created it
        original_role = self.user.profile.role
        
        # Modify the profile
        self.user.profile.role = "professor"
        self.user.profile.save()
        
        # Refresh from database to verify
        updated_profile = Profile.objects.get(pk=self.user.profile.pk)
        self.assertEqual(updated_profile.role, "professor")


# this needs to be edited
# class RedirectTestCase(TestCase):
#     def setUp(self):
#         """Set up test client and test data"""
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username="testuser",
#             password="testpass123"
#         )
#         self.profile = self.user.profile

#     def test_redirect_to_login_when_not_authenticated(self):
#         """Test that unauthenticated users are redirected to login"""
#         # Access a view that requires authentication
#         response = self.client.get(reverse('your-view-name'))  # Replace with actual view name
        
#         # Check for redirect status code (302 for temporary redirect)
#         self.assertEqual(response.status_code, 302)
#         # Check redirect location (typically to login page)
#         self.assertIn('/accounts/login/', response.url)
#         # Or use Django's built-in assertion
#         self.assertRedirects(response, '/accounts/login/?next=/your/path/')

#     def test_redirect_after_successful_login(self):
#         """Test redirect after user logs in"""
#         # Login the user
#         self.client.login(username='testuser', password='testpass123')
        
#         # Access a view that redirects after login
#         response = self.client.get(reverse('your-view-name'))
        
#         # Verify redirect status
#         self.assertEqual(response.status_code, 302)
#         # Verify redirect destination
#         self.assertRedirects(response, '/expected/destination/')

#     def test_redirect_with_permanent_redirect_status(self):
#         """Test permanent redirect (301)"""
#         response = self.client.get(reverse('old-url-name'))
        
#         self.assertEqual(response.status_code, 301)
#         self.assertRedirects(response, '/new-url/', fetch_redirect_response=False)

#     def test_redirect_preserves_query_parameters(self):
#         """Test that redirects preserve query parameters"""
#         response = self.client.get(reverse('your-view-name') + '?next=/dashboard/')
        
#         self.assertEqual(response.status_code, 302)
#         self.assertIn('next=/dashboard/', response.url)

#     def test_authenticated_user_not_redirected_to_login(self):
#         """Test that authenticated users are not redirected to login"""
#         # Login first
#         self.client.login(username='testuser', password='testpass123')
        
#         # Access protected view
#         response = self.client.get(reverse('protected-view'))
        
#         # Should NOT redirect to login (status code should be 200)
#         self.assertEqual(response.status_code, 200)
#         # Should not be a redirect
#         self.assertNotEqual(response.status_code, 302)


# # Example with Profile view redirects
# class ProfileViewRedirectTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username="testuser",
#             password="testpass123"
#         )
#         self.profile = self.user.profile

#     def test_redirect_to_profile_on_unauthenticated_access(self):
#         """Test unauthenticated users redirected to profile creation"""
#         response = self.client.get(reverse('profile-detail'))
        
#         self.assertEqual(response.status_code, 302)
#         self.assertContains(response, 'accounts/login')

#     def test_authenticated_user_sees_profile(self):
#         """Test authenticated users can access their profile"""
#         self.client.login(username='testuser', password='testpass123')
        
#         response = self.client.get(reverse('profile-detail'))
        
#         self.assertEqual(response.status_code, 200)
#         self.assertNotEqual(response.status_code, 302)