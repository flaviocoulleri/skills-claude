# CG Cloud Conceptual Data Models

Detailed descriptions of each functional area, its objects, their purpose, and how they relate to each other.

## Table of Contents
1. [Customer Master](#customer-master)
2. [Organization Unit](#organization-unit)
3. [Customer Sets & Segmentation](#customer-sets--segmentation)
4. [Asset](#asset)
5. [Product Master](#product-master)
6. [Product Assortment](#product-assortment)
7. [User / Substitution](#user--substitution)
8. [Advanced Promotions](#advanced-promotions)
9. [Visit Planning](#visit-planning)
10. [Activity Planning](#activity-planning)
11. [Activity Execution](#activity-execution)
12. [Advanced Order](#advanced-order)
13. [Penny Perfect Pricing](#penny-perfect-pricing)
14. [Customer Task](#customer-task)
15. [Inventory Control](#inventory-control)

---

## Customer Master

The Customer Master area manages all customer-related data in CG Cloud.

### Objects and Descriptions

- **Account** — Standard Salesforce Account, represents the customer (trade organization or store)
- **Trade Org Hierarchy** — Time-dependent hierarchy relation between accounts (trade organizations and stores). Allows modeling of chains, regions, and individual stores with validity dates.
- **Account Relationship** — Business partner role relations between accounts. Supports roles like Wholesaler, Bill-To, Payer, and Delivery Recipient.
- **Sales Org** — Data segregation by market. Controls which data is visible to which market/country.
- **Customer Extension** — CPG-specific extensions of the standard Account object. Stores business partner roles and CPG-specific attributes not on the standard Account.
- **Customer Visit Settings** — Visit plan parameters per account. Controls how automatic visit planning works for each customer.
- **POS (Point of Sale)** — Information about a place in customer's premises (secondary placement) where goods are sold to consumers. Examples: end-cap display, cooler location, shelf section.
- **Customer Org Unit** — Time-dependent assignment between customer and Org Units/territories.
- **Customer Manager** — Time-dependent and management-type-specific user assignments to accounts. Supports types like sales, merchandising, and service.
- **Listing Classification** — Classification for product listings at the customer level.
- **Account Receivable** — Tracks receivables per customer.
- **Customer Template** — Template controlling customer instance behavior.
- **Operating Hours** — Standard Salesforce object for customer operating hours.
- **Contact** — Standard Salesforce Contact linked to the Account.

### Key Relationships
```
Account ← Trade Org Hierarchy (parent-child between accounts)
Account ← Account Relationship (partner roles: wholesaler, bill-to, payer, delivery)
Account ← Customer Extension (CPG-specific fields)
Account ← Customer Org Unit → Org Unit (territory assignment)
Account ← Customer Manager → User (sales rep assignment)
Account ← Customer Visit Settings (visit planning config)
Account ← POS (in-store placements)
Account ← Sales Org (market segregation)
```

---

## Organization Unit

Manages the manufacturer's organizational structure (territories).

### Objects and Descriptions

- **Org Unit** — Holds detail of the manufacturer's organization structure. Territories organized by different types (sales, merchandising, service).
- **Org Unit Hierarchy** — Time-dependent territory structure. Holds the relationship between two org units based on flexible levels.
- **Customer Org Unit** — Time-dependent assignment of customer to Org Units.
- **Org Unit User** — Time-dependent assignment of users to org units.
- **Customer Manager** — Time-dependent relation by management type. Specific user assignments to accounts (sales, merchandising, service).
- **Flatten Org Unit Hierarchy** — Flat hierarchy of the dynamic hierarchy holding node information. Created and updated via batch process for performance.
- **Sales Org** — Data segregation by market.

### Key Relationships
```
Org Unit ← Org Unit Hierarchy (parent-child between territories)
Org Unit ← Org Unit User → User (rep assigned to territory)
Org Unit ← Customer Org Unit → Account (customer in territory)
Org Unit → Sales Org (market)
Flatten Org Unit Hierarchy ← batch process from Org Unit Hierarchy
```

---

## Customer Sets & Segmentation

Groups of accounts that can be assigned to promotions, activities, or pricing conditions.

### Objects and Descriptions

- **Sales Org** — Data segregation by market.
- **Customer Set** — Group of accounts which can be assigned to a promotion, activity, or pricing condition.
- **Customer Set Customer** — Junction object between Customer (Account) and Customer Set.
- **Segmentation Rule** — User filter criteria used to create the customer segmentation. Contains a link to the Customer Set object where the list of accounts is stored.
- **Promotion** — Agreements between a CPG manufacturer and a retailer chain to increase revenue/market share via mechanics like temporary price reductions or in-store displays.
- **Pricing Condition** — Consolidated object with all kind of pricing conditions used by penny perfect pricing.
- **Activity** — List of questions/surveys to be answered during visit.
- **Activity Customer Set** — Junction object between Job Definition List (Activity) and Customer Set.

### Key Relationships
```
Customer Set ← Customer Set Customer → Account (members)
Customer Set ← Segmentation Rule (auto-population criteria)
Customer Set ← Promotion (assigned to promotion)
Customer Set ← Pricing Condition (assigned to pricing)
Customer Set ← Activity Customer Set → Activity (assigned to activity)
Customer Set → Sales Org
```

---

## Asset

Physical elements with value that the manufacturer places at a customer location.

### Objects and Descriptions

- **Asset Template** — Manage different asset types (cooler types, fridge types, etc.).
- **Asset** — Physical element placed at a customer. E.g., cooler, fridge with serial number, purchase date, and other information.
- **POS** — Information of a place in customer's premises where the asset is located.
- **Sales Org** — Data segregation by market.
- **Asset Audit** — Asset tracking and audit details. Used for periodic verification of asset condition and location.
- **Customer Task** — Reference for asset-related customer tasks like asset service requests (e.g., cooler repair).

### Key Relationships
```
Asset → Asset Template (type definition)
Asset → Account (placed at customer)
Asset → POS (specific location in store)
Asset ← Asset Audit (audit records)
Asset ← Customer Task (service requests)
Asset → Sales Org
```

---

## Product Master

Product catalog and hierarchy management.

### Objects and Descriptions

- **Sales Org** — Data segregation by market.
- **Product Template** — Templates for creating products with similar attributes.
- **Product Hierarchy** — Made up of product groups with product at lowest level.
- **Unit of Measure** — Logistical unit of product (case, each, pallet, etc.).
- **Conditions** — Product prices for order value calculation.
- **Product Manager** — Promotion planner must be an active product manager with read/write access for at least one product category.
- **Product Parts / BOM (Bill of Material)** — Product bundles, defining component products.
- **Warehouse Products** — Relationship between warehouse and product.

### Key Relationships
```
Product2 → Product Template (type definition)
Product2 ← Product Hierarchy (category structure)
Product2 ← Unit of Measure (packaging units)
Product2 ← Product Part (BOM components)
Product2 ← Conditions / Pricing (prices)
Product2 ← Warehouse Product → Warehouse
Product2 → Sales Org
```

---

## Product Assortment

Manages which products are listed (available) at which customers.

### Objects and Descriptions

- **Product Assortment Template** — Controls behavior of assortment instances. Sales organization dependent.
- **Product Assortment** — Assortment header.
- **Product Assortment Customer** — Assigned to any node in the account hierarchy.
- **Product Assortment Product** — Time-dependent product assignments with additional attributes such as customer-specific product numbers.
- **Listing Modules** — Definition of store types by trade organization.
- **Product Modules** — Store module specific product assignment with target values such as facings or price.
- **Product Assortment Store** — Flattened store listing, valid for the current day. Created via batch process.

### Key Relationships
```
Product Assortment → Product Assortment Template
Product Assortment ← Product Assortment Customer → Account
Product Assortment ← Product Assortment Product → Product2
Listing Module ← Product Module → Product2
Product Assortment Store (flattened by batch, current day only)
```

---

## User / Substitution

Manages user assignments to sales organizations and absence handling.

### Objects and Descriptions

- **Sales Org User** — Relationship between user and Sales Org.
- **Sales Org** — Data segregation by market.
- **Substitution** — Manage planned and unplanned absence of users (vacation, illness).
- **Customer Substitution** — Splitting substitutions across different accounts. Allows partial substitution where different reps cover different accounts.

### Key Relationships
```
User ← Sales Org User → Sales Org
User ← Substitution (absence record)
Substitution ← Customer Substitution → Account (per-account substitute)
```

---

## Advanced Promotions

Trade promotion management between CPG manufacturer and retailers.

### Objects and Descriptions

- **Promotion Template** — Controls behavior of different promotion types (e.g., Special Promotion).
- **Tactic Template** — Controls the behavior of a tactic.
- **Tactic** — Describes the mechanics of a promotion. Exactly 1 tactic per promotion in Retail Execution.
- **Tactic Product** — Promoted products at tactic level with details such as quantities and hurdle classification.
- **Account** — Promotion link to a single account (typically a trade organization node).
- **Customer Sets** — Promotion link to a set of accounts/stores.
- **Activity** — Reference from one to many activities to a promotion.
- **Sales Folder** — Reference from promotion to sales folders (sell sheets).

### Key Relationships
```
Promotion → Promotion Template
Promotion ← Tactic → Tactic Template
Tactic ← Tactic Product → Product2
Promotion → Account (single account) OR Customer Set (group)
Promotion ← Activity (linked surveys/tasks)
Promotion ← Promotion Sales Folder → Sales Folder
Promotion → Sales Org
```

---

## Visit Planning

Scheduling and managing field rep visits to customers.

### Objects and Descriptions

- **Visit** — Tracks information related to a field rep's visit to an account. Includes customer and non-customer specific calls (sales visit, private appointment).
- **Event** — Customer visits have a 1:1 relation to Event. Non-customer visits are events only.
- **Visit Template** — Manage multiple visit types (sales visit, phone call, vacation).
- **Trip List** — Reusable visit lists.
- **Trip List Customer** — Used to plan visits based on a predefined sequence of customers.
- **Job Lists** — Explicit task list of activities for a visit.
- **Customer Visit Setting** — Account settings for automatic visit planning.
- **Sales Organization User** — User-specific settings for visit planning.

### Key Relationships
```
Visit → Visit Template (visit type)
Visit → Account (customer visited)
Visit → User (field rep)
Visit ↔ Event (1:1 for customer visits)
Trip List ← Trip List Customer → Account (route)
Visit ← Job Lists (activities to execute)
Account ← Customer Visit Setting (planning config)
```

---

## Activity Planning

Configuring surveys, questions, and tasks that field reps execute during visits.

### Objects and Descriptions

- **Data Type** — Specifies the answer format (text, number, toggle, photo, etc.).
- **Data Type Option** — Options for toggle-type questions.
- **Job Template** — Specifies type of activity.
- **Job Definition Template** — Specifies question/survey question.
- **Template Question** — Question assigned to activity template.
- **Activity Template** — Pre-configured list of job definition templates.
- **Promotion** — Reference to advanced promotion.
- **POS Template** — Specifies the POS type.
- **Activity** — List of questions/surveys to be answered during visit.
- **Visit Template** — Specifies the type of visit.
- **Field Sales Activity** — Bundle of activities.
- **Activity Product** — Products assigned to activity.
- **Activity Customer** — Customers assigned to activity.
- **Activity Customer Set** — Customer Sets assigned to activity.

### Key Relationships
```
Activity Template ← Template Question → Job Definition Template → Job Template
Job Definition Template → Data Type (answer format)
Activity → Activity Template (configuration source)
Activity ← Activity Product → Product2
Activity ← Activity Customer → Account
Activity ← Activity Customer Set → Customer Set
Activity → Promotion (linked promotion)
Activity → Visit Template
Field Sales Activity → Activity (bundle)
```

---

## Activity Execution

What happens when a field rep actually performs activities during a visit.

### Objects and Descriptions

- **Visit Job** — Contains responses of questions/survey questions captured during visit execution. This is where the actual answers are stored.
- **Visit** — Represents the store visit made by the Sales Representative.
- **Question** — Question assigned to the activity to be answered during visit execution.
- **Job List** — List of jobs generated from non-standard/event-based activities.
- **POS** — Represents Points of Sales/Secondary Placements.

### Key Relationships
```
Visit ← Visit Job (answers captured)
Visit Job → Question (which question was answered)
Visit Job → POS (which placement was checked)
Visit Job → Product2 (which product was surveyed)
Visit Job → Activity (which activity was executed)
```

---

## Advanced Order

Order capture during field visits.

### Objects and Descriptions

- **Order Template** — Manage different types of orders (standard, indirect, return).
- **Item Type** — Manage line item types within an order (standard quantities, free item).
- **Order Header** — Header details including reference to visit, customer, wholesaler, order and delivery date.
- **Order Items** — Ordered products with quantities and references to unit of measure, promotion, pricing.
- **Wholesaler** — Account with the broker role.
- **Product Assortment** — From type 'Listing' or 'Sales Assortment'.
- **Signature** — Digital signature captured at order completion.

### Key Relationships
```
Order → Order Template (order type)
Order → Account (customer)
Order → Account/Wholesaler (broker)
Order → Visit (captured during visit)
Order ← Order Item → Product2
Order Item → Unit of Measure
Order Item → Promotion (linked deal)
Order ← Signature
Order → Sales Org
```

---

## Penny Perfect Pricing

SAP-style pricing engine for exact price calculation.

### Key Concept
The master system for pricing conditions is always external (typically SAP). CG Cloud receives pricing data and applies it during order capture.

### Objects and Descriptions

- **Pricing Procedure** — Follows SAP pricing structure. Defines the sequence of condition types to apply.
- **Condition Types and Access Sequence** — Following SAP pricing terminology.
- **Key Type** — Optimized structure for all conditions. Defines the combination of fields (the key) that identifies an individual pricing condition record.
- **Complex Pricing Condition** — Optimized format of all pricing conditions. Generated by batch process (`ScheduleCGCloudServiceComplexPricing`).
- **Calculation Schema** — Defines how prices are calculated step by step.
- **Calculation Schema Steps** — Individual steps in the calculation.
- **Search Strategy** — Defines how to find the right condition record.
- **Key Attribute** — Building blocks for Key Type. Standard keys like customer, product, and more specific configurable keys.

### Integration Flow
```
External ERP (SAP) → Staging Tables:
  - Pricing Condition Stage (Header Record)
  - Pricing Condition Scale Stage (Scales + Free Products)
→ Batch Process (ScheduleCGCloudServiceComplexPricing)
→ Complex Pricing Condition (optimized for runtime)
```

### Key Relationships
```
Calculation Schema ← Calculation Schema Steps (pricing steps)
Calculation Schema ← Calculation Schema Determination (which schema to use)
Search Strategy ← Search Strategy Steps → Key Type
Key Type ← Key Attribute (field combinations)
Complex Pricing Condition uses: Account hierarchy, Product hierarchy, Sales Org, Promotions, Customer Set
```

---

## Customer Task

Task management for field operations.

### Objects and Descriptions

- **Customer Task** — Manage all kinds of customer tasks from the sales rep or supervisor.
- **Customer Task Template** — Controls types of tasks (complaint, service request, etc.).
- **Substitution** — Link to absence management for task reassignment.
- **Asset** — Reference to asset object for service requests (e.g., cooler repair).

### Key Relationships
```
Customer Task → Customer Task Template (task type)
Customer Task → Account (customer)
Customer Task → User (assigned rep)
Customer Task → Asset (for service requests)
Customer Task → Substitution (reassignment during absence)
Customer Task → Sales Org
```

---

## Inventory Control

Stock tracking for van sales, delivery, and warehouse operations.

### Objects and Descriptions

- **Inventories** — Can be defined for product stock, customer quota, or to track cash flow. Assignable to Tour, Vehicle, Users, Accounts, or combinations.
- **Inventory Transactions** — Created for every trigger that changes inventory (give products away, collect money). Allows tracking of accurate inventory for distributed and offline shared inventories.
- **Order Item Inventory Transaction** — Defines if a certain Item Type is relevant for changing an inventory, how (increase/decrease), and which inventory. Distinguishes between returns that can be sold again vs. blocked stock.
- **Inventory Control Document** — Defines the purpose of the document and the used Item Templates. Supports use cases: Pre-Order, Van Sales, Delivery, Check-out, Check-in, Truck Audit, Truck Transfer.

### Key Relationships
```
Inventory → Tour, Vehicle, Account, User (assignment)
Inventory ← Inventory Transaction (stock movements)
Inventory Transaction → Product2
Order Item ← Order Item Inventory Transaction → Inventory
Inventory Control Document → Item Templates
Inventory → Sales Org
```

---

## Enhanced Data Model: Harmonized vs Net New Objects

The CG Cloud Enhanced Data Model introduced changes in two categories:

### Harmonized Areas (existing objects refined)
- Product Hierarchy
- User Setting / Sales Org User / Sales Org
- Account Hierarchy / Account Extensions / Account Relationship / Account Manager / Account Sales Data / Account Org Unit / Account Visit Setting
- Product Assortment (Assortment Customer, Assortment Product, Assortment Order Template, Assortment Template)
- Visit (Visit Template)
- Promo & Tactic (Tactic Template, Tactic, Tactic Product)
- Advanced Order (Order Item, Order Payment, Order Template, Order Item Template, Order Payment Template)

### Net New Objects
- Product Master, Product Unit of Measure, Product Template
- Customer Master, Account Template
- Enhanced Master Data (Account Set User, Customer Set, Customer Set Organization Unit, Hierarchy, Organization Unit User, Organization Unit)
- Listing Modules
- POS Template, POS
- Promotional Rewards (Promotion Expression, Promotion Reward, Promotion Hurdle, Promotion Reward Product, Promotion Reward Group)
- Penny Perfect Pricing (Calculation Schema, Determination, Calculation Schema Step, Search Strategy, Key Types, Pricing Condition, Pricing Condition Template)
- Sales Folders (Sales Folder Template, Sales Folder, Sell Sheets)
- Signature (Signature Template)
- System Number, Field Sales Activity
- Advanced Activities (Visit Job, Data Type, Job Definition Template, Job List, Activity Template, Activity Customer Set, Job Template, Segmentation Rule, Substitution/Customer Substitution, Segmentation Rule Definition)
- Daily Report (Daily Report, Daily Report Template)
- Inventory (Inventory, Inventory Transaction, Inventory Template)
- Asset (Asset Audit, Asset Template, Activity Product, Asset Activity, Customer Task)
- Picture
- Tasks (Customer Tasks, Key Types, Condition Scale Stage, Condition Stage, Operating Hours, Task Management, Account Receivables)
