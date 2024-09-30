#!/usr/bin/env python3

import csv
import argparse
from datetime import datetime

# Function to read data from CSV files
def read_csv_files(acquisitions_file, sales_file):
    acquisitions = []
    sales = []
    
    # Read acquisitions CSV
    with open(acquisitions_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            acquisitions.append({
                "date": datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S %Z").replace(hour=0, minute=0, second=0, microsecond=0),
                "price": float(row["price"]),
                "quantity": float(row["quantity"])
            })
    
    # Read sales CSV
    with open(sales_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sales.append({
                "date": datetime.strptime(row["date"], "%m/%d/%y"),
                "price": float(row["price"]),
                "quantity": float(row["quantity"])
            })
    
    return acquisitions, sales

# Calculate profits and losses
def calculate_transactions(acquisitions, sales, verbose):
    transactions = []

    # Copy acquisitions list to track remaining quantities
    remaining_acquisitions = [acq.copy() for acq in acquisitions]

    do_reverse = False
    sales.sort(key=lambda x: x["date"], reverse=do_reverse)
    remaining_acquisitions.sort(key=lambda x: x["price"], reverse=True)
    #print(sales)

    total_unaccounted_quantity = 0
    total_unaccounted_sales = 0

    total_profit_loss = 0
    for sale in sales:
        quantity_to_sell = sale["quantity"]
        new_transactions = []
        acquisitions_to_remove = []
        for (i, acquisition) in enumerate(remaining_acquisitions):
            # Check that the sale date is after the acquisition date
            date_valid = sale["date"] >= acquisition["date"]
            if verbose and date_valid:
                print("checking sale.date: {} acquisition.date: {} quantity: {:>8,.2f} date.valid? {}".format(sale["date"], acquisition["date"], acquisition["quantity"], date_valid))
            if sale["date"] >= acquisition["date"] and acquisition["quantity"] > 0:
                # Determine the quantity sold from this acquisition
                quantity_sold = min(quantity_to_sell, acquisition["quantity"])
                
                # Calculate profit or loss for the quantity sold
                profit_loss = (sale["price"] - acquisition["price"]) * quantity_sold

                total_profit_loss += profit_loss
                
                new_transactions.append({
                    "acquisition_date": acquisition["date"],
                    "sale_date": sale["date"],
                    "acquisition_price": acquisition["price"],
                    "sale_price": sale["price"],
                    "quantity_sold": quantity_sold,
                    "total_profit_loss": profit_loss
                })

                # Update remaining quantity to sell and acquisition quantity
                quantity_to_sell -= quantity_sold
                acquisition["quantity"] -= quantity_sold
                #if acquisition["quantity"] < 0.0001:
                #    acquisitions_to_remove.append(i)

                # If all quantity is sold, break the loop
                if quantity_to_sell == 0:
                    break
        if quantity_to_sell != 0:
            print("Unaccounted for sale of asset!: {} {} {:,.2f}".format(sale["date"], sale["price"], quantity_to_sell))
            total_unaccounted_quantity += quantity_to_sell
            total_unaccounted_sales += 1
        else:
            if verbose:
                print("Sold all of {:,} sold on {}".format(sale["quantity"], sale["date"]))
        if verbose:
            print("Transactions:")
            for t in new_transactions:
                print("  acq.date: {} quantity: {:,.2f} profit: {:,.2f}".format(t["acquisition_date"], t["quantity_sold"], t["total_profit_loss"]))
            for i in sorted(acquisitions_to_remove, reverse=True):
                del(acquisitions[i])
            print("")
        transactions.extend(new_transactions)

    print("total_profit_loss from {} sales: {:,.2f}".format(len(sales), total_profit_loss))
    print("unaccounted_total: {} unaccounted_quantity: {}".format(total_unaccounted_sales, total_unaccounted_quantity))
    # Sort by lowest profit or highest loss
    transactions.sort(key=lambda x: x["total_profit_loss"])

    return transactions

def main(acquisitions_file, sales_file, verbose):
    # Read data from CSV files
    acquisitions, sales = read_csv_files(acquisitions_file, sales_file)

    # Calculate transactions
    transactions = calculate_transactions(acquisitions, sales, verbose)

    if transactions:
        print("Transactions sorted by lowest profit or highest loss:")
        for trans in transactions:
            profit_loss = "Profit" if trans['total_profit_loss'] > 0 else "Loss"
            print(f"Acquired on {trans['acquisition_date']} at ${trans['acquisition_price']}\n"
                  f"  and sold on {trans['sale_date']} at ${trans['sale_price']}\n"
                  f"  for quantity {trans['quantity_sold']:,.2f} resulting in a {profit_loss} of ${trans['total_profit_loss']:,.2f}")
    else:
        print("No transactions found.")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Calculate profit and loss from asset sales.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Print more information")
    parser.add_argument('acquisitions_file', help="Path to the CSV file containing acquisitions data.")
    parser.add_argument('sales_file', help="Path to the CSV file containing sales data.")
    
    args = parser.parse_args()
    
    # Run the main function
    main(args.acquisitions_file, args.sales_file, args.verbose)

