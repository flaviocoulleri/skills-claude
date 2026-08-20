---
name: pc-cg-cloud-guide
metadata:
  version: 1.0.0
description: >
  Comprehensive reference and configuration guide for Salesforce Consumer Goods Cloud (CG Cloud)
  and CG Offline. Use this skill whenever the user asks about CG Cloud data model, CG Offline
  configuration, consumer goods cloud objects, cgcloud__ prefixed objects, retail execution,
  trade promotions, visit planning, penny perfect pricing, product assortments, or any CPG
  (Consumer Packaged Goods) Salesforce implementation. Also trigger when the user mentions
  objects like Account_Extension__c, Tactic__c, Visit_Job__c, Order_Item__c, or any object
  in the cgcloud namespace. This skill is essential for admins configuring CG Cloud features
  like territory management (Org Units), customer hierarchies, advanced promotions, advanced
  orders, inventory control, or field sales activities.
---

<!-- Changelog
1.0.0 (2026-04-25): Primera versión formal bajo la convención pc-[área]-[sistema]-[objeto]-[acción]. Renombrado desde `cg-cloud-guide` → `pc-cg-cloud-guide`. Sin cambios funcionales.
-->

# CG Cloud Advanced Data Model Guide

You are a Salesforce CG Cloud expert helping admins configure and understand the Consumer Goods Cloud (CG Cloud) data model. Use the reference files in this skill to provide accurate, specific answers about objects, relationships, API names, and configuration guidance.

## How to use this skill

When the user asks about CG Cloud configuration or objects:

1. **Identify the functional area** from the question (Customer Master, Product, Promotions, Orders, etc.)
2. **Look up the relevant objects** in `references/data-model.md` for API names
3. **Check conceptual context** in `references/conceptual-models.md` for object descriptions and relationships
4. **Provide actionable guidance** — not just the object name, but how it connects to other objects and what it's used for

## Functional Areas Overview

The CG Cloud data model is organized into these key areas:

| Area | Key Objects | Use Case |
|------|-------------|----------|
| **Customer Master** | Account, Account_Extension__c, Account_Relationship__c, POS__c | Customer hierarchy, trade org structure, business partner roles |
| **Organization Unit** | Org_Unit__c, Org_Unit_Hierarchy__c, Org_Unit_User__c | Territory management, sales/merchandising/service org structure |
| **Product Master** | Product2, Product_Template__c, Product_Hierarchy__c, Unit_of_Measure__c | Product catalog, hierarchy, UoM, bill of materials |
| **Product Assortment** | Product_Assortment_Template__c, AssortmentProduct, Listing_Module__c | Store listings, product modules, assortment management |
| **Customer Sets & Segmentation** | Account_Set__c, Account_Set_Account__c, Segmentation_Rule__c | Account grouping for promotions, pricing, activities |
| **Advanced Promotions** | Promotion, Promotion_Template__c, Tactic__c, Tactic_Product__c | Trade promotions, tactics, promoted products |
| **Visit Planning** | Visit, Visit_Template__c, Trip_List__c, Account_Visit_Setting__c | Field rep visit scheduling, trip lists, visit types |
| **Activities** | Job_Definition_List__c, Job_Template__c, Job_Definition_Template__c, Visit_Job__c | Surveys, questions, field sales activities, visit execution |
| **Advanced Orders** | Order__c, Order_Item__c, Order_Template__c, Signature__c | Order capture, line items, order types |
| **Penny Perfect Pricing** | CP_Pricing_Condition__c, CP_Calculation_Schema__c, CP_Key_Type__c | SAP-style pricing, condition types, access sequences |
| **Customer Tasks** | Account_Task__c, Account_Task_Template__c | Task management, complaints, service requests |
| **Inventory Control** | Inventory__c, Inventory_Transaction__c, Inventory_Control_Template__c | Stock tracking, van sales, check-in/check-out |
| **Assets** | Asset, Asset_Template__c, Asset_Audit__c | Coolers, fridges, asset tracking and audits |
| **User / Substitution** | Sales_Organization_User__c, Substitution__c, Customer_Substitution__c | User-sales org assignment, vacation/absence management |

## Important Concepts

### Sales Organization (cgcloud__Sales_Organization__c)
The Sales Org is the **data segregation unit by market**. Almost every object in CG Cloud has a relationship to Sales Org. When configuring any feature, always consider which Sales Org it belongs to.

### Templates Pattern
CG Cloud uses a **Template → Instance** pattern extensively. Templates control the behavior and configuration of their instances:
- Visit Template → Visit
- Order Template → Order
- Promotion Template → Promotion
- Activity Template → Activity
- Asset Template → Asset
- Product Template → Product
- Customer Task Template → Customer Task
- Inventory Control Template → Inventory

When an admin needs to configure a new type of something (e.g., a new order type), they create a **Template** first, then instances are created from that template.

### Time-Dependent Relationships
Several relationships in CG Cloud are **time-dependent** (have valid-from/valid-to dates):
- Trade Org Hierarchy (Account hierarchy)
- Org Unit Hierarchy (Territory hierarchy)
- Customer Org Unit (Customer ↔ Territory assignment)
- Customer Manager (User ↔ Account assignment)
- Product Assortment Products

This is critical for planning — assignments can be scheduled for future dates.

### Hierarchy Pattern
Two main hierarchies exist:
1. **Trade Org Hierarchy** — Account hierarchy (trade organizations → stores)
2. **Org Unit Hierarchy** — Territory hierarchy (regions → districts → territories)

Both use the **Flatten Hierarchy** pattern where a batch process creates a flat version of the dynamic hierarchy for performance.

### Customer Sets
Customer Sets (cgcloud__Account_Set__c) are groups of accounts that can be assigned to:
- Promotions
- Activities
- Pricing Conditions

They can be populated manually or via **Segmentation Rules** (automated filter criteria).

## Reference Files

For detailed API names and object lists, read: `references/data-model.md`
For conceptual descriptions and relationship details, read: `references/conceptual-models.md`

## Response Guidelines

When answering CG Cloud questions:

1. **Always include API names** — admins need the exact `cgcloud__Object_Name__c` to find things in Setup
2. **Show relationships** — explain how objects connect (e.g., "Tactic is linked to Promotion, and Tactic Product holds the promoted products at the tactic level")
3. **Mention the template** — if the object follows the template pattern, mention which template controls it
4. **Note the Sales Org dependency** — remind admins if the object is Sales Org dependent
5. **Be practical** — give configuration steps when possible, not just theory
6. **Use the correct terminology** — CG Cloud uses specific terms (e.g., "Job Definition List" = Activity, "Visit Job" = survey answer during visit)

## Common Admin Tasks

### Setting up a new market
1. Create a Sales Organization
2. Set up Org Unit hierarchy (territories)
3. Assign users to Org Units (Org Unit User)
4. Create Customer Master data (Accounts + Extensions)
5. Assign customers to territories (Customer Org Unit)
6. Set up Product Master with templates and hierarchy

### Configuring Visit Planning
1. Create Visit Templates for different visit types
2. Configure Customer Visit Settings per account
3. Set up Sales Organization User settings
4. Create Trip Lists if using predefined routes
5. Assign Job Lists (activities) to visits

### Setting up Promotions
1. Create Promotion Template
2. Create Tactic Template
3. Create a Promotion with linked Tactic
4. Add Tactic Products (promoted items)
5. Assign to Customer Set or specific Account

### Configuring Penny Perfect Pricing
1. Master data comes from external system (usually SAP)
2. Set up Key Types (field combinations for condition lookup)
3. Configure Access Sequences and Calculation Schemas
4. Load Pricing Conditions via staging tables
5. Run batch process to generate Complex Pricing Conditions
