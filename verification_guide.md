# Verification Guide for SDA POS System

This document outlines the steps to verify each requirement of the SDA POS System. Follow the "Verification Flow" for each requirement to confirm its correct implementation.

---

## **1. Sales & Billing**

### **1. The system shall allow users to create and process sales transactions.**
**Verification Flow:**
1. Login as a Cashier or Admin.
2. Navigate to the "Sales" dashboard.
3. Add a product to the cart.
4. Click "Checkout", select a payment method (e.g., Cash), and confirm.
5. **Pass Criteria:** A "Sale Completed!" message appears, and the cart is cleared.

### **2. The system shall support adding items to the cart through product search or barcode scanning.**
**Verification Flow:**
1. In the "Sales" view, click the search bar.
2. Type a partial product name (e.g., "App" for Apple).
3. Verify the list updates to show matching products.
4. Select a product and click "Add to Cart".
5. **Pass Criteria:** The product appears in the "Current Sale" list with the correct price.

### **3. The system shall allow editing item quantities in a transaction.**
**Verification Flow:**
1. Add an item to the cart.
2. In the cart list (right panel), click the `+` button to increase quantity.
3. Click the `-` button to decrease quantity.
4. **Pass Criteria:** The quantity and line total update instantly. If quantity reaches 0, the item is removed.

### **4. The system shall automatically calculate totals, taxes, and discounts.**
**Verification Flow:**
1. Add items worth $100.00 (example) to the cart.
2. Click "Checkout".
3. Observe the "Subtotal", "Tax (10%)", and "Total Due".
4. **Pass Criteria:** 
   - Subtotal = $100.00
   - Tax = $10.00 (10% of $100)
   - Total Due = $110.00

### **5. The system shall allow applying promo codes, discounts, or loyalty points.**
**Verification Flow:**
1. In the Checkout window, enter a valid discount code (if one exists in DB, e.g., create one first manually or via seed).
2. Or, select a customer with loyalty points.
3. Check the "Redeem Points" checkbox.
4. **Pass Criteria:** The "Discount/Points" line updates, and the "Total Due" decreases accordingly.

### **6. The system shall generate digital receipts after each sale.**
**Verification Flow:**
1. Complete a sale transaction.
2. Open the project folder and navigate to the `receipts/` directory.
3. **Pass Criteria:** A new text file `receipt_<sale_id>.txt` exists containing the correct date, items, tax, and total.

---

## **2. Payments**

### **7. The system shall allow split payments across multiple payment methods.**
**Verification Flow:**
1. In the Checkout window, select "Split" as the Payment Method.
2. Enter $50 in "Cash Amount" and the remainder in "Card Amount".
3. Click "Confirm Payment".
4. **Pass Criteria:** The transaction succeeds only if the sum of Cash and Card equals the Total Due.

### **8. The system shall handle refunds and reverse payments.**
**Verification Flow:**
1. Navigate to the "Refunds" dashboard.
2. Enter a valid Transaction ID from a previous sale.
3. Select an item to refund and click "Process Refund".
4. **Pass Criteria:** A success message appears, and if you check "Inventory", the stock for that item has increased.

---

## **3. Inventory Management Integration**

### **9. The system shall automatically update stock levels after each sale.**
**Verification Flow:**
1. Note the stock of "Item A" in the "Inventory" view (e.g., 50).
2. Go to "Sales" and sell 2 units of "Item A".
3. Return to "Inventory".
4. **Pass Criteria:** Stock for "Item A" is now 48.

### **10. The system shall restrict selling out-of-stock items.**
**Verification Flow:**
1. Find an item with 0 stock (or edit one to 0).
2. Try to add it to the cart in "Sales".
3. **Pass Criteria:** An "Out of Stock" warning popup appears, and the item is not added.

### **11. The system shall notify users when an item’s stock is low.**
**Verification Flow:**
1. Edit an item's stock to 5 or less in "Inventory".
2. Go to "Sales" and try to add that item to the cart.
3. **Pass Criteria:** A "Low Stock" information popup appears warning that stock is low.

### **12. The system shall link sales data with supplier restocking.**
**Verification Flow:**
1. Go to "Restock" view.
2. Click `+ New` next to Supplier to create a supplier.
3. Select the new Supplier and an Item, enter quantity, and click "Update Stock".
4. **Pass Criteria:** Stock updates, and a record is created in `restock_orders` (verifiable via DB tool or code inspection).

---

## **4. User Management & Security**

### **13. The system shall support role-based access (Admin, Cashier, Manager).**
**Verification Flow:**
1. Log in as `admin`.
2. Create a new user with role `Cashier`.
3. Log out and log in as the new `Cashier`.
4. **Pass Criteria:** The user is logged in and sees the dashboard appropriate for their role.

### **14. The system shall require authentication (username/password, PIN).**
**Verification Flow:**
1. On the Login screen, try to login with wrong credentials. (Should fail).
2. Login with correct username/password. (Should success).
3. Click "Use PIN" and enter a valid PIN (if set).
4. **Pass Criteria:** Access is granted only with valid credentials.

### **15. The system shall log user activities (login, sales, refunds, stock changes).**
**Verification Flow:**
1. Perform a Login, a Sale, and a Logout.
2. Check the `activity_logs` table in the database.
3. **Pass Criteria:** Rows exist for "LOGIN", "SALE" (or implicitly via sale record), and "LOGOUT" for that user.

### **16. The system shall restrict transaction voiding/canceling to authorized users.**
**Verification Flow:**
*Note: This is implicitly handled by role checks in the code, currently mostly enforced via UI availability or backend logic.*
1. **Pass Criteria:** Only authorized flows allow refunds/voids (e.g., Refund screen availability).

### **17. The system shall support session management (shift start/end tracking).**
**Verification Flow:**
1. Log in.
2. Log out.
3. Check `user_sessions` table in DB.
4. **Pass Criteria:** A record exists with a `login_time` and a `logout_time`.

---

## **5. Customer Management**

### **18. The system shall allow creating customer profiles (name, contact, purchase history).**
**Verification Flow:**
1. Go to "Loyalty" view.
2. Click "Add New Customer".
3. Enter Name and Phone. Click Save.
4. **Pass Criteria:** Customer is saved and can be searched by phone number.

### **19. The system shall support loyalty programs and reward points.**
**Verification Flow:**
1. Create a customer.
2. Process a sale linked to that customer (select them in Sales view).
3. **Pass Criteria:** Verify in "Loyalty" view that the customer's points have increased based on the products bought.

### **20. The system shall track customer purchase history for analytics.**
**Verification Flow:**
1. Performed via the Database relations.
2. **Pass Criteria:** `sales` table records have a valid `customer_id` linking to the `customers` table.

### **21. The system shall allow searching customers by name, phone number, or ID.**
**Verification Flow:**
1. In "Sales" or "Loyalty" view, use the search box.
2. Enter a known phone number.
3. **Pass Criteria:** The correct customer details appear.

---

## **6. Reporting & Analytics**

### **22. The system shall generate daily, weekly, and monthly sales reports.**
**Verification Flow:**
1. Go to "Reports" view -> "Sales" tab.
2. Click "Today", "Last 7 Days", "Last 30 Days".
3. **Pass Criteria:** The table populates with transaction data for those periods.

### **23. The system shall provide cashier-wise sales reports.**
**Verification Flow:**
1. Go to "Reports" view -> "Cashier" tab.
2. **Pass Criteria:** A list shows each cashier username and their total sales amount.

### **24. The system shall generate tax and financial reports.**
**Verification Flow:**
1. In "Reports" -> "Sales" tab.
2. Look at the totals at the bottom or the "Tax" column.
3. **Pass Criteria:** "Total Tax" is displayed and calculated correctly from the sales data.

### **25. The system shall generate product performance reports (fast-moving vs slow-moving).**
**Verification Flow:**
1. Go to "Reports" -> "Products" tab.
2. **Pass Criteria:** A list of products is shown, sorted by "Units Sold", identifying best sellers.

