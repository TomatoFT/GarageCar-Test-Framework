#!/usr/bin/env bash
# Clone and bootstrap the GarageCar demo application.
set -euo pipefail

APP_DIR="${APP_DIR:-$(cd "$(dirname "$0")/../.." && pwd)/GarageCar}"
REPO_URL="${REPO_URL:-https://github.com/TomatoFT/GarageCar.git}"

echo "==> App directory: $APP_DIR"

if [ ! -d "$APP_DIR/.git" ]; then
  echo "==> Cloning GarageCar..."
  git clone --depth 1 "$REPO_URL" "$APP_DIR"
else
  echo "==> GarageCar already cloned, skipping git clone"
fi

cd "$APP_DIR"

if [ ! -d ".venv" ]; then
  echo "==> Creating Python virtual environment..."
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q -r requirements/dev.txt

echo "==> Running migrations and seeding..."
python manage.py migrate
python manage.py seed_business_rules

echo "==> Creating demo user (opera / 1)..."
if ! python manage.py create_demo_user 2>/dev/null; then
  echo "==> create_demo_user failed; using shell fallback..."
  python manage.py shell -c "
from django.contrib.auth.models import Group, User
from apps.accounts.models import StaffProfile
user, _ = User.objects.get_or_create(username='opera', defaults={'email': 'opera@example.com'})
user.set_password('1')
user.is_staff = True
user.is_superuser = True
user.first_name = 'Demo'
user.last_name = 'User'
user.save()
group, _ = Group.objects.get_or_create(name='ADMIN')
group.user_set.add(user)
StaffProfile.objects.update_or_create(
    user=user,
    defaults={
        'first_name': 'Demo',
        'last_name': 'User',
        'email': 'opera@example.com',
        'mobile': '0900000000',
        'address': 'Demo Address',
        'is_admin': True,
    },
)
print('Demo user ready')
"
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
if [ -f "$ROOT_DIR/scripts/seed_e2e_data.py" ]; then
  echo "==> Seeding E2E data (Toyota brand + labor rate)..."
  python "$ROOT_DIR/scripts/seed_e2e_data.py"
fi

echo ""
echo "Setup complete. Start the app:"
echo "  cd $APP_DIR && source .venv/bin/activate && python manage.py runserver"
echo ""
echo "Login at http://127.0.0.1:8000/login/  (opera / 1)"
echo ""
echo "Important: start runserver AFTER setup so labor rates appear in repair forms."
