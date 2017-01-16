#!/usr/bin/python3

import unittest


class CashRegister:
    def __init__(self, twenties, tens, fives, twos, ones):
        if twenties >=0 and tens >= 0 and fives >= 0 and twos >= 0 and ones >= 0:
            self.twenties = twenties
            self.tens = tens
            self.fives = fives
            self.twos = twos
            self.ones = ones
        else:
            self.twenties = 0
            self.tens = 0
            self.fives = 0
            self.twos = 0
            self.ones = 0

    def put(self, twenties, tens, fives, twos, ones):
        self.twenties += twenties
        self.tens = +tens
        self.fives += fives
        self.twos += twos
        self.ones += ones
        return self

    def take(self, twenties, tens, fives, twos, ones):
        if (twenties <= self.twenties and tens <= self.tens and fives <= self.fives and twos <= self.twos
                and ones <= self.ones and twenties >= 0 and tens >= 0 and fives >= 0 and twos >= 0 and ones >= 0):
            self.twenties -= twenties
            self.tens -= tens
            self.fives -= fives
            self.twos -= twos
            self.ones -= ones
            return 0
        else:
            print("Not enough currency, or negative values passed in")
            return -1

    def show(self):
        print(self.twenties * 20 + self.tens * 10 + self.fives * 5 + self.twos * 2 + self.ones,
              self.twenties, self.tens, self.fives, self.twos, self.ones)

    def _make_change_helper(self, amount, extra_twos):
        t_ones = 0
        t_twos = 0 + extra_twos
        t_fives = 0
        t_tens = 0
        t_twenties = 0
        while t_twenties < self.twenties and amount >= 20:
            amount -= 20
            t_twenties += 1
        while t_tens < self.tens and amount >= 10:
            amount -= 10
            t_tens += 1
        while t_fives < self.fives and amount >= 5:
            amount -= 5
            t_fives += 1
        while t_twos < self.twos and amount >= 2:
            amount -= 2
            t_twos += 1
        while t_ones < self.ones and amount >= 1:
            amount -= 1
            t_ones += 1

        if amount == 0:
            self.ones = self.ones - t_ones
            self.twos = self.twos - t_twos
            self.fives = self.fives - t_fives
            self.tens = self.tens - t_tens
            self.twenties = self.twenties - t_twenties

        return {"remaining": amount,
                "ones": t_ones,
                "twos":  t_twos,
                "fives": t_fives,
                "tens": t_tens,
                "twenties": t_twenties}

    def change(self, amount):
        if amount < 1:
            print("Cannot give change less than one dollar")
            return -1
        ret = self._make_change_helper(amount, 0)
        # if we cannot make exact change - it may be because our greedy algorithm fails due to two dollar bills
        # catch this corner case by manually injecting two dollar bills, then running same algorithm until we
        # exhaust possibilities of two dollar bills
        if ret["remaining"] == 0:
            self.take(ret["twenties"], ret["tens"], ret["fives"], ret["twos"], ret["ones"])
            return 0
        else:
            extra_twos = 1
            while extra_twos <= self.twos and ret["remaining"] != 0:
                amount -= 2
                ret = self._make_change_helper(amount, extra_twos)
                extra_twos += 1
            if ret["remaining"] == 0:
                self.take(ret["twenties"], ret["tens"], ret["fives"], ret["twos"] + extra_twos, ret["ones"])
                return 0
            else:
                print("Could not make change")
                return -1


class TestCashRegister(unittest.TestCase):
    def test_put(self):
        x = CashRegister(0, 0, 0, 0, 0)
        x.put(1, 1, 1, 1, 1)
        self.assertEqual(x.twenties, 1)
        self.assertEqual(x.tens, 1)
        self.assertEqual(x.fives, 1)
        self.assertEqual(x.twos, 1)
        self.assertEqual(x.ones, 1)

    def test_take(self):
        x = CashRegister(10, 10, 10, 10, 10)
        x.take(1, 2, 3, 4, 5)
        self.assertEqual(x.twenties, 9)
        self.assertEqual(x.tens, 8)
        self.assertEqual(x.fives, 7)
        self.assertEqual(x.twos, 6)
        self.assertEqual(x.ones, 5)

    def test_show(self):
        x = CashRegister(10, 10, 10, 10, 10)
        x.show()

    def test_cannot_make_change(self):
        x = CashRegister(10, 10, 10, 10, 10)
        self.assertEqual(x.change(400), -1)
        self.assertEqual(x.twenties, 10)
        self.assertEqual(x.tens, 10)
        self.assertEqual(x.fives, 10)
        self.assertEqual(x.twos, 10)
        self.assertEqual(x.ones, 10)

    def test_change1(self):
        x = CashRegister(10, 10, 10, 10, 10)
        self.assertEqual(x.change(310), 0)
        self.assertEqual(x.twenties, 0)
        self.assertEqual(x.tens, 0)
        self.assertEqual(x.tens, 0)
        self.assertEqual(x.fives, 8)
        self.assertEqual(x.twos, 10)
        self.assertEqual(x.ones, 10)

    def test_change2(self):
        x = CashRegister(0, 0, 1, 3, 0)
        self.assertEqual(x.change(6), 0)
        self.assertEqual(x.twenties, 0)
        self.assertEqual(x.tens, 0)
        self.assertEqual(x.fives, 1)
        self.assertEqual(x.twos, 0)
        self.assertEqual(x.ones, 0)

    def test_change3(self):
        x = CashRegister(0, 1, 1, 2, 1)
        self.assertEqual(x.change(13), 0)
        self.assertEqual(x.twenties, 0)
        self.assertEqual(x.tens, 0)
        self.assertEqual(x.fives, 1)
        self.assertEqual(x.twos, 1)
        self.assertEqual(x.ones, 0)

    def test_change4(self):
        x = CashRegister(0, 0, 1, 4, 0)
        self.assertEqual(x.change(8), 0)
        self.assertEqual(x.twenties, 0)
        self.assertEqual(x.tens, 0)
        self.assertEqual(x.fives, 1)
        self.assertEqual(x.twos, 0)
        self.assertEqual(x.ones, 0)

    def test_check_negative_constructor_call(self):
        x = CashRegister(0, -1, 1, 4, -1)
        self.assertEqual(x.twenties, 0)
        self.assertEqual(x.tens, 0)
        self.assertEqual(x.fives, 0)
        self.assertEqual(x.twos, 0)
        self.assertEqual(x.ones, 0)

    def test_check_negative_take_call(self):
        x = CashRegister(0, 1, 1, 1, 1)
        self.assertEqual(x.take(-1, 0, 0, 0, 0), -1)
        self.assertEqual(x.twenties, 0)
        self.assertEqual(x.tens, 1)
        self.assertEqual(x.fives, 1)
        self.assertEqual(x.twos, 1)
        self.assertEqual(x.ones, 1)

    def test_check_negative_change_call(self):
        x = CashRegister(0, 1, 1, 1, 1)
        self.assertEqual(x.change(-15), -1)
        self.assertEqual(x.twenties, 0)
        self.assertEqual(x.tens, 1)
        self.assertEqual(x.fives, 1)
        self.assertEqual(x.twos, 1)
        self.assertEqual(x.ones, 1)

if __name__ == '__main__':
    unittest.main()
