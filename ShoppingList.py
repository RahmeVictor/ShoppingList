#!/usr/bin/python3
import csv
from functools import partial
from statistics import *
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext


# TODO: Use scrolled text instead of labels to show Data

def read_data(showPriceHistory):
    itemsData = []
    itemsDataHistory = []
    priceHistory = []
    try:
        with open(dataFilePath, 'r', newline='') as testFile:
            pass

    except FileNotFoundError:
        # Create empty file
        with open(dataFilePath, 'w', newline='') as newFile:
            fileCreator = csv.writer(newFile, delimiter=',', quotechar='|')
            fileCreator.writerow('')

    with open(dataFilePath, 'r', newline='') as dataFile:
        dataReader = csv.reader(dataFile, delimiter=',', quotechar='|')
        rowNumber = 0
        for row in dataReader:
            rowNumber += 1
            try:
                item = row[0]
                quantity = int(row[1])
                for price in row[2:]:
                    price = float(price)
                    if price.is_integer():
                        price = int(price)

                    priceHistory.append(price)

                if showPriceHistory:
                    itemDataHistory = [item, quantity] + priceHistory
                    itemsDataHistory.append(itemDataHistory)

                else:
                    priceAverage = float(median(priceHistory))
                    if priceAverage.is_integer():
                        priceAverage = int(priceAverage)

                    itemsData.append([item, quantity, priceAverage])

                priceHistory = []

            except ValueError:
                # TODO: Automagically fix this
                messagebox.showwarning('Warning!',
                                       'Error reading row (line): {}, with the contents: {}.'.format(rowNumber, row))

    if showPriceHistory:
        return itemsDataHistory

    else:
        # Returns [[item, quantity, priceAverage], [item, quantity, priceAverage]]
        return itemsData


def save_data(event):
    found = False
    inputItem = str(itemEntry.get())
    inputQuantity = int(quantityEntry.get())
    inputPrice = float(priceEntry.get())
    if inputPrice.is_integer():
        inputPrice = int(inputPrice)

    itemsDataHistory = read_data(showPriceHistory=True)
    priceHistory = []
    for itemData in itemsDataHistory:
        if itemData[0] == inputItem:
            found = True
            priceHistory.extend(itemData[2:])
            priceHistory.append(inputPrice)
            inputItemData = [inputItem, inputQuantity] + priceHistory
            itemsDataHistory.remove(itemData)
            itemsDataHistory.append(inputItemData)
            break

        else:
            found = False

    if not found:
        priceHistory.append(inputPrice)
        inputItemData = [inputItem, inputQuantity] + priceHistory
        itemsDataHistory.append(inputItemData)

    with open(dataFilePath, 'w', newline='') as dataFile:
        dataWriter = csv.writer(dataFile, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        for itemData in itemsDataHistory:
            dataWriter.writerow(itemData)

    # Update the show list menu
    data_menu()


def delete_data(event, dataLabels):
    itemsData = read_data(showPriceHistory=False)
    with open(dataFilePath, 'w', newline='') as dataFile:
        dataWriter = csv.writer(dataFile, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        for itemData in itemsData:
            item = itemData[0]
            quantity = itemData[1]
            price = itemData[2]
            if str(itemEntry.get()) != item:
                dataWriter.writerow([item, quantity, price])

    data_menu()


def data_menu_old(dataLabels):
    for label in dataLabels:
        # Destroy all previous item Labels to refresh them
        label.destroy()

    showColumn = 0
    showRow = 3
    xMinSize = 965  # Min size of display
    yMinSize = 50
    # Creates a label for each item and it's quantity
    for itemData in read_data(showPriceHistory=False):
        # Make a Label for each item
        item = itemData[0]
        quantity = itemData[1]
        priceAverage = itemData[2]
        showItemData = item, quantity, priceAverage
        dataDisplay = Label(root, text=showItemData)
        dataDisplay.grid(row=showRow, column=showColumn)
        dataLabels.append(dataDisplay)
        if showColumn == 7:
            # Label wrapping
            showColumn = 0
            showRow += 1
            # Increase minimum size
            yMinSize += 30
            root.minsize(xMinSize, yMinSize)

        else:
            showColumn += 1
            root.minsize(xMinSize, yMinSize)


def data_menu():
    showData = scrolledtext.ScrolledText(root, width=20, height=20)
    showData.grid(row=1, column=0)
    itemCount = 0
    textLine = 0
    allItemInfo = ''
    for itemData in read_data(showPriceHistory=False):
        item = itemData[0]
        quantity = str(itemData[1])
        priceAverage = str(itemData[2])

        itemInfo = '{0} {1} {2}'.format(item, quantity, priceAverage)
        allItemInfo = '{0}{1}\n'.format(allItemInfo, itemInfo)
#        if itemCount == 5:
#            allItemInfo = allItemInfo, '/n'
#            textLine += 1
#            itemCount = 0

    showData.insert(INSERT, allItemInfo)


root = Tk()
root.title('Shopping list')
root.minsize(1080, 200)
dataFilePath = 'data.csv'
dataLabels = []

# ------Main Menu------

# TODO: make function out of this (actually harder than it looks like)

data_menu()

Label(root, text='Item|Quantity|Avg Price').grid(row=0, column=0, sticky=W)
Label(root, text='Item:').grid(row=0, column=1, sticky=W, padx=4)
itemEntry = Entry(root)
itemEntry.grid(row=0, column=2, sticky=W, padx=4)

Label(root, text='Quantity:').grid(row=0, column=3, sticky=W, padx=4)
quantityEntry = Entry(root)
quantityEntry.grid(row=0, column=4, sticky=W, padx=4)

Label(root, text='Price:').grid(row=0, column=5, sticky=W, padx=4)
priceEntry = Entry(root)
priceEntry.grid(row=0, column=6, sticky=W, padx=4)

submitButton = Button(root, text='Add Item')
submitButton.grid(row=0, column=7, sticky=W, padx=4)
submitButton.bind('<Button-1>', save_data)

deleteButton = Button(root, text='Delete Item')
deleteButton.grid(row=0, column=8, sticky=W, padx=4)
deleteButton.bind('<Button-1>', partial(delete_data, dataLabels=dataLabels))  # partial(func, arg)

root.bind('<Return>', save_data)

root.mainloop()
