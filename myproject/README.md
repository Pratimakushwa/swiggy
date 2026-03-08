# Food Delivery Clone (Swiggy-like)

This Django project implements a basic food delivery application with both customer and admin panels. It includes user registration/login, restaurant/menu browsing, cart/checkout functionality, order tracking, and a simple admin dashboard with CRUD operations.

## Setup

1. **Activate virtual environment** (already created under `env`):
   ```powershell
   env\Scripts\activate
   ```

2. **Install dependencies** (if any additional packages are needed, e.g., Pillow for image uploads):
   ```powershell
   pip install django pillow
   ```

   *Note:* this skeleton is currently configured for **local static/dummy
images only**. Cloudinary entries were removed from `INSTALLED_APPS` to avoid
errors – if you later want to add cloud storage, simply reinstall the
packages and re‑add them yourself.
3. **Run migrations**
   ```powershell
   cd myproject
   python manage.py migrate
   ```

4. **Create a superuser** to access Django admin and mark staff accounts:
   ```powershell
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```powershell
   python manage.py runserver
   ```

   Then open http://127.0.0.1:8000 in your browser.

## Customer Panel

- **Sign up** at `/signup/` and **login** at `/login/`.
- **Home page** displays categories and search bar.
- **Restaurant list** at `/restaurants/` allows filtering by name, location, or category.
- **Restaurant menu** and ability to add items to cart.
- **Cart** page at `/cart/` lets users update quantities or proceed to checkout.
- **Checkout** requires address and payment method (COD/online).
- After placing an order, users can **track** it at `/order/<id>/track/`.

> Cart is restricted to a single restaurant; adding an item from a different restaurant will clear previous cart contents.

## Admin Panel

Staff users (created via superuser or marked in admin) can access a custom admin dashboard at `/admin-dashboard/`.

Features available to staff:

- **Dashboard** showing totals (users, restaurants, orders, pending orders).
- **Manage Restaurants**: add, edit, delete.
- **Manage Food Items**: add, edit, delete.
- **Manage Orders**: view orders and update status.

Regular Django admin (`/admin/`) remains available for advanced management.

## Notes

- Uploaded food images are stored in the `media/` directory by
default. When Cloudinary is enabled they will go to the cloud instead.
  A local placeholder (`main/static/main/img/dummy.svg`) is now used for
  restaurants/food items that do not have an image, so you can add a
  `static/main/img/dummy.svg` file or swap the existing one with your own.
- The UI uses Bootstrap via CDN for basic styling.
- This implementation is meant for development; security, payments, and production considerations are out of scope.

Feel free to enhance functionality and style to match the wireframes in your design.