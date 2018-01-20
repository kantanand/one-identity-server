from django.contrib.auth.models import User;
from datacenter.models import UserProfile;
user,status = User.objects.get_or_create(username='admin@identity.com');
user.email = 'admin@identity.com';
user.first_name = 'Admin';
user.last_name = 'User';
user.is_active = True;
user.is_superuser = True;
user.is_staff = True;
user.set_password('adminblock@123#');
user.save();
user_profile = UserProfile.objects.get(user=user);
user_profile.is_admin = True;
user_profile.save();
exit();

