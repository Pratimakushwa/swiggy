# Complete Admin Panel Guide

## 🔐 How to Create an Admin User

### Method 1: Using Django Admin (Recommended)

1. First, create a **superuser** (admin account):
   ```powershell
   cd myproject
   python manage.py createsuperuser
   ```
   - Follow prompts to create username, email, password
   - This account has full access

2. Go to Django Admin: `http://127.0.0.1:8000/admin/`
   - Login with superuser credentials

3. For **converting a regular user to admin**:
   - Click **"Users"** in admin
   - Find the user you want to make admin
   - Check the **"Staff status"** checkbox
   - Click **"Save"**
   - That user can now access admin panel

---

## 📊 Admin Dashboard Features

Once logged in as a staff user, click **"Admin Dashboard"** in navbar to access:

### 1. **Dashboard Stats**
   - 👥 Total Users - count of all registered users
   - 🍽️ Total Restaurants - count of all restaurants
   - 📦 Total Orders - count of all orders
   - ⏳ Pending Orders - orders with "Placed" status

### 2. **Quick Links**
   - 🏪 Manage Restaurants
   - 🍕 Manage Food Items
   - 📬 Manage Orders

---

## 🏪 Manage Restaurants

### View All Restaurants
1. Click **"Manage Restaurants"** from dashboard
2. See table with: Name, Location, Rating, Delivery Time, Actions

### Add Restaurant
1. Click **"+ Add Restaurant"** button
2. Fill in:
   - **Restaurant Name:** e.g., "Pizza Palace"
   - **Location:** e.g., "Downtown Indore"
   - **Rating:** 0-5 (decimal)
   - **Delivery Time:** minutes (e.g., 30)
   - **Average Price:** ₹ for two people
   - **Categories:** Select multiple (Ctrl+Click on Mac/Linux, Shift+Click for range)
3. Click **"💾 Save Restaurant"**

### Edit Restaurant
1. Click **"✏️ Edit"** button on any restaurant
2. Update fields
3. Click **"💾 Save Restaurant"**

### Delete Restaurant
1. Click **"🗑️ Delete"** button
2. Confirm deletion
3. ⚠️ This cannot be undone!

---

## 🍕 Manage Food Items

### View All Food Items
1. Click **"Manage Food Items"** from dashboard
2. See table with: Name, Restaurant, Price, Availability, Actions

### Add Food Item
1. Click **"+ Add Food Item"** button
2. Fill in:
   - **Restaurant:** Select from dropdown
   - **Name:** e.g., "Margherita Pizza"
   - **Description:** e.g., "Classic cheese pizza"
   - **Price:** ₹299
   - **Image:** (Optional - upload photo or leave empty for dummy)
   - **Available:** Check box if item is available
3. Click **"💾 Save Food Item"**

### Edit Food Item
1. Click **"✏️ Edit"** on any item
2. Update price, description, availability, etc.
3. Click **"💾 Save Food Item"**
4. **Changing Price:** Edit the price field and save - instantly updates in cart

### Delete Food Item
1. Click **"🗑️ Delete"** button
2. Confirm deletion

---

## 📬 Manage Orders

### View All Orders
1. Click **"Manage Orders"** from dashboard
2. See table with: Order ID, Customer, Restaurant, Total Price, Status, Date, Actions

### Order Statuses
- ⏳ **Placed** - Customer just placed the order
- 👨‍🍳 **Preparing** - Restaurant is cooking
- 🚚 **Out for Delivery** - Delivery in progress
- ✓ **Delivered** - Order completed
- ✗ **Cancelled** - Order was cancelled

### Update Order Status
1. Click **"📝 Update Status"** on any order
2. See order details:
   - Order ID
   - Customer name
   - Restaurant
   - Total price
   - Date & time placed
3. Select new status from dropdown
4. Click **"✓ Update Status"**
5. Status updates instantly

---

## 🔑 Admin Navbar

When logged in as a staff user:
- **Home** - Go to public home page
- **Restaurants** - View all restaurants (customer view)
- ~~Cart~~ - Hidden for admin users
- **Admin Dashboard** - Access admin panel
- **Logout** - Sign out

---

## 📝 Best Practices

1. **Before Opening:** Make sure you have:
   - At least 1 restaurant created
   - At least 1 food item in that restaurant
   - Then customers can order

2. **Managing Orders:**
   - Check dashboard for pending orders count
   - Update status as soon as restaurant confirms
   - Move to "Delivered" when actually delivered

3. **Food Items:**
   - `Available` checkbox - uncheck if out of stock
   - Customers can't order unavailable items
   - Can hide items without deleting

4. **Images:**
   - Currently uses dummy/placeholder images
   - Upload real images from food item edit form
   - Images will appear in restaurant menus

---

## 🆘 Troubleshooting

### "Admin Dashboard" button not showing?
- Make sure you're logged in as a staff user
- Ask superuser to mark you as staff in admin panel

### Can't access `/admin/`?
- You need superuser account
- Create one with: `python manage.py createsuperuser`

### Form won't submit?
- Check all **required fields** are filled (marked with *)
- Make sure price is a number
- Check for validation error messages

---

## 🚀 Workflow Example

1. **New Order Comes In:**
   - Customer places order
   - You see it in "Manage Orders" with "Placed" status

2. **Restaurant Cooking:**
   - Click "Update Status" 
   - Change to "Preparing"

3. **Ready to Deliver:**
   - Change to "Out for Delivery"

4. **Delivered:**
   - Change to "Delivered"

5. **Track Stats:**
   - Dashboard shows fewer pending orders
   - Total orders count increases

---

**Everything is fully styled and ready to use!** 🎉

Go to http://127.0.0.1:8000/ and login with your staff account to get started!
