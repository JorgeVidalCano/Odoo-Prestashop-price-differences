class PricePR_Odoo:

	""" This script ajusts automatically the difference in price between prestashop and odoo """

	def __init__(self, pr_total, pr_tax, odoo_unitPrice, odoo_tax_list, odoo_quantity, odoo_discount):
		self.pr_total = pr_total
		self.pr_tax = pr_tax
		self.odoo_unitPrice = odoo_unitPrice
		self.odoo_tax_list = odoo_tax_list
		self.odoo_quantity = odoo_quantity
		self.odoo_discount = odoo_discount

	def odooPrice(self):
		""" Prices for odoo. it gets the sum of the price with no taxes, with taxes and also the amount of tax """ 
		sum_odoo_noTax = sum(self.odoo_unitPrice)
		sum_odoo_Tax = sum(x*y for x, y in zip(self.odoo_tax_list, self.odoo_unitPrice))
		odoo_tax = round(sum_odoo_Tax - sum_odoo_noTax, 2)

		return sum_odoo_noTax, sum_odoo_Tax, odoo_tax
		
	def highestVatSelector(self): 
		""" Selects the position where the price with 21% is """
		new = [(x,y) for x, y in zip(self.odoo_tax_list, self.odoo_unitPrice)]
		newList = []

		for i in range(0,len(new)):
			if 1.21 in new[i]:
				newList.append(i)

		## In case there are no products with 21%
		if newList == []:
			newList = range(0,len(new))
		return newList

	def priceAjuster(self):
		sum_odoo_noTax, sum_odoo_Tax, odoo_tax = self.odooPrice()	

		steps = 0
		inc = 0.01
		if odoo_tax > pr_tax:
			inc = -0.01

		positionList = self.highestVatSelector()
		positionChange = 0
		while round(odoo_tax, 2) != pr_tax:
						
			sum_odoo_noTax, sum_odoo_Tax, odoo_tax = self.odooPrice()	

			if positionChange > len(positionList)-1:
				positionChange = 0
			self.odoo_unitPrice[positionList[positionChange]] += inc

			positionChange += 1
			steps += 1

			## emergency exit
			if steps == 100005:
				break

		bono_descuento = (pr_total - sum_odoo_Tax)
		precio_cantidad = [(precio/cantidad) for precio, cantidad in zip(self.odoo_unitPrice, self.odoo_quantity)]
		resultado = []
		
		for precio, descuento in zip(precio_cantidad, odoo_discount):
			if descuento != 0:
				resultado.append(round((precio/((float(100-descuento)/100))), 3))
			else:
				resultado.append(precio)

		print("New prices: {}.\nAdd discount: {}".format(self.odoo_unitPrice, bono_descuento))	

		return self.odoo_unitPrice, bono_descuento

pr_total = 96.65
pr_tax = 9.06
odoo_unitPrice = [-3.49, -0.37, 77.23, 8.22]
odoo_tax_list = [1.1, 1.21, 1.1, 1.21]
odoo_quantity = [1, 1, 1, 1]
odoo_discount = [0, 0, 0, 0]
				

prices = PricePR_Odoo(pr_total, pr_tax, odoo_unitPrice, odoo_tax_list, odoo_quantity, odoo_discount)

prices.priceAjuster()

