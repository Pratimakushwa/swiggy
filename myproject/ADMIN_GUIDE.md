# Django Admin Panel Guide

## Access Admin Panel
1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials

## If you don't have a superuser yet:
```powershell
cd myproject
python manage.py createsuperuser
```
Follow the prompts to create username, email, and password.

---

## Managing Restaurants

1. Click on **"Restaurants"** in the admin sidebar
2. Click **"Add Restaurant"** button
3. Fill in:
   - **Name**: e.g., "Pizza Palace"
   - **Location**: e.g., "Downtown Indore"
   - **Rating**: 4.5 (decimal between 0-5)
   - **Delivery Time**: 30 (minutes)
   - **Average Price**: 300.00 (₹)
   - **Categories**: Select multiple categories (Ctrl+Click)
4. Click **"Save"**

---

## Managing Categories

1. Click on **"Categories"** in the admin sidebar
2. Click **"Add Category"** button
3. Fill in:
   - **Name**: e.g., "North Indian"
   - **Slug**: e.g., "north-indian" (auto-generates)
4. Click **"Save"**

---

## Managing Food Items

1. Click on **"Food Items"** in the admin sidebar
2. Click **"Add Food Item"** button
3. Fill in:
   - **Restaurant**: Select from dropdown
   - **Name**: e.g., "Margherita Pizza"
   - **Description**: e.g., "Classic cheese pizza"
   - **Price**: 299.00
   - **Image**: (Optional - upload or leave empty for dummy image)
   - **Available**: Check this box (default: checked)
4. Click **"Save"**

---

## Notes

- **Dummy Images**: All images throughout the app use a local static placeholder (`main/static/main/img/dummy.svg`). When you upload real images, they'll automatically display.
- **Restaurant Carousel**: Shows the first 5 restaurants on homepage with scroll navigation
- **Food Categories**: Display as circular icons on homepage for filtering
- **Menu Pages**: Show all food items for a restaurant in a responsive grid

---

## Dashboard Stats

The **Admin Dashboard** (`/admin-dashboard/`) shows:
- Total users
- Total restaurants  
- Total orders
- Pending orders

Available only to staff users.

---

## Quick Tips

- Use **Search** boxes in admin to find restaurants/items quickly
- **Filter** by restaurant when viewing food items
- **Bulk delete** items by selecting checkboxes and using "Delete" action
- Click restaurant name to edit its details and associated categories
