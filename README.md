# Cloth Store

This is a Django-based cloth store web application, featuring product search & filtering, a shopping cart, user profiles with order history, reviews & ratings, 
and an admin dashboard.

## Features
- **Product Search & Filtering**: Users can search for clothing items by name or category.
- **Shopping Cart**: Users can add and remove products from their cart.
- **User Profiles & Order History**: Users can view their past orders.
- **Reviews & Ratings**: Users can leave feedback on products.
- **Admin Dashboard**: Admins can manage products, orders, and users.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tutujnr/cloth-store.git
   cd ecommerce-django
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server:**
   ```bash
   python manage.py runserver
   ```

## Usage
- Register or log in as a user.
- Browse and search for products.
- Add products to the cart and proceed to checkout.
- View past orders and leave reviews.

## Admin Dashboard
- Navigate to `/admin/` and log in as the superuser.
- Manage products, orders, and users.
