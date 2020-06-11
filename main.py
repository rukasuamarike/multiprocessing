import sys
import multiprocessing
import threading

def main():
    testlist = [Customer("a"), Customer("b"), Customer("c"), Customer("d"), Customer("e"), Customer("f")]
    jim = Service([], "jim")
    bob = Cashier(testlist, "bob", jim)
    jim.assistant = bob
    cash = multiprocessing.Process(target=bob.work)
    serve = multiprocessing.Process(target=jim.work)
    cash.start()
    serve.start()
    cash.join()
    serve.join()


class Worker:
    has_customers = False
    has_order = False
    customer = None
    customers = None
    on_shift = True

    def __init__(self, customers, name):
        self.customers = customers
        self.name = name
        self.on_shift = True

    def take_order(self, customer):
        self.customer = customer
        self.has_customers = True
        self.customer.has_order = False
        print("{} has taken {}'s order".format(self.name, self.customer.name))
        self.has_order = True


class Cashier(Worker):

    def __init__(self, customers, name, assistant):
        Worker.__init__(self, customers, name)
        self.assistant = assistant

    def pass_order(self, customer):
        if self.has_customers:
            print("{} paid and gave order to {}".format(customer.name, self.name))
            self.assistant.has_order = True
            print("{} has passed order to {}".format(self.name, self.assistant.name))
            self.assistant.customers.append(customer)
            self.assistant.has_customers = True
            print("{} has moved to {}'s line".format(customer.name, self.assistant.name))
            # actually removing customers from list messes up the loop so I did not do that
            print("{} has been removed from {}'s list".format(customer.name, self.name))
            self.has_order = False

    def check_time(self):
        if len(self.customers) > 0:
            self.on_shift = True

    def work(self):
        if self.on_shift:
            while len(self.customers) > 0:
                customer = self.customers[0]
                self.on_shift = True
                k = self.customers.index(customer)
                self.has_order = True
                self.take_order(customer)
                self.pass_order(customer)
                del self.customers[k] # (this was how I removed)
        self.check_time()


class Service(Worker):
    def __init__(self, customers, name):
        Worker.__init__(self, customers, name)
        self.assistant = None

    def do_order(self, customer):
        customer.has_goods = True
        print("{} has given {} their requested goods".format(self.name, customer.name))
        self.has_order = False
        self.customers.remove(customer)

    def check_time(self):
        if self.assistant.on_shift:
            self.on_shift = True

    def work(self):
        if self.on_shift:
            print(self.customers)
            while len(self.customers) > 0:
                self.has_customers = True
                self.do_order(self.customers[0])
        self.check_time()


class Customer:
    has_order = True
    has_goods = False
    name = ""
    index = 0

    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    main()
