# ☕ Product Optimization & Revenue Contribution Analysis

A complete **data analytics project** focused on understanding product performance, revenue contribution, and menu optimization for a coffee retail business.

---

## 📌 Project Overview

This project analyzes transaction-level data from a coffee retailer to answer:

- Which products drive the most revenue?
- Which products are popular but not profitable?
- How concentrated is revenue across the menu?
- Which items should be optimized or removed?

The goal is to **improve decision-making using data instead of intuition**.

---

## 🎯 Objectives

### Primary Objectives
- Identify top & bottom selling products
- Measure revenue contribution per product
- Analyze category-level performance
- Evaluate revenue concentration (Pareto)

### Secondary Objectives
- Detect "Hero" products
- Identify low-performing SKUs
- Support menu optimization strategy

---

## 📊 Key KPIs

- **Product Revenue Contribution (%)**
- **Sales Volume**
- **Category Revenue Share**
- **Revenue Concentration Ratio**
- **Product Efficiency (Revenue per Unit)**

---

## 📁 Dataset

| Column | Description |
|-------|------------|
| transaction_id | Unique transaction |
| transaction_qty | Quantity sold |
| unit_price | Price per item |
| product_category | Category (Coffee, Tea, etc.) |
| product_type | Sub-category |
| product_detail | Specific product |
| store_location | Store location |

---

## 📈 Analysis Performed

### 1️⃣ Product Performance
- Top & bottom products (Revenue + Volume)
- Product ranking

### 2️⃣ Revenue Contribution
- Product-wise revenue share
- Category contribution

### 3️⃣ Pareto Analysis (80/20)
- Identify revenue-driving products
- Detect long-tail items

### 4️⃣ Demand Analysis
- Revenue by hour
- Category demand heatmap

### 5️⃣ Product Segmentation
- Hero Products (High revenue + High sales)
- Potential Products
- Dead Products

---

## 📊 Visualizations

- 📌 Bar Charts → Top/Bottom products  
- 📌 Pie Chart → Category revenue share  
- 📌 Treemap → Product contribution  
- 📌 Scatter Plot → Sales vs Revenue  
- 📌 Pareto Chart → Revenue concentration  
- 📌 Heatmap → Demand patterns  

---

## 🖥️ Dashboard (Streamlit)

Interactive dashboard built using **Streamlit** with:

- Filters (Category, Product Type, Location)
- Top-N Product selection
- Dynamic KPIs
- Drill-down product analysis

### ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 💡 Key Insights
- A small % of products generate majority revenue (Pareto principle)
- Some high-volume products contribute low revenue → pricing issue
- Long-tail products add complexity but little value
- Menu optimization can improve efficiency & profits

## 🚀 Business Recommendations
- Focus on top-performing products
- Remove or redesign low-impact items
- Optimize pricing for high-volume products
- Bundle slow-moving products

## 🛠️ Tech Stack

Python
Pandas
NumPy
Matplotlib
Seaborn
Plotly
Streamlit

## 📂 Project Structure

📦 Afficionado-coffee-roaster/
│
├── app.py                                  # Streamlit dashboard
├── Afficionado Coffee Roasters.xlsx        # Data file
├── Final_research_paper.pdf                # Final report
└── README.md                               # Documentation

## 👤 Author

**Pratham Rangoonwala**  
Data Analyst | Python | Streamlit