import unittest
import numpy

class BanditProblem:
    def __init__(self,num_of_days,num_of_restaurants):
        self.num_of_days = num_of_days #how many days we visit each restaurant
        self.num_of_restaurants = num_of_restaurants #how many restaurant options there are
        self.probabilities = self.generate_probabilities() #variable storing the range of probabilities
        self.best_satisfaction = self.best_possible_satisfaction() #the best possible value from the range of distributions if you picked the most optimal choice

    #Method to generate the probabilities for each restaurant
    def generate_probabilities(self):
        ranges = [] #creates an array
        for i in range (self.num_of_restaurants): #iterates for how many restaurants there are
            low = numpy.random.uniform(0,0.7) #generates a random number between 0 and 1 for lower bound
            high = numpy.random.uniform(low,1) #use uniform to make sure upper bound is larger than the lower bound
            ranges.append((low,high))#into the array append the the range of potential satisfaction
        return ranges #returns the array
    
    #Method to find the best probability index
    def best_possible_satisfaction(self):
        upperboundsatisfaction = 0 #highest upper bound currently
        for i in range(self.num_of_restaurants): #loop through all the probabilities
            low,high = self.probabilities[i] #get the upper bound value
            if high > upperboundsatisfaction: #compare the upper bound value of the current restaurant, if it is higher
                upperboundsatisfaction = high #set this as the current highest upper bound value

        return upperboundsatisfaction #return the value

class BanditProblemStrategies:
    def __init__(self,probabilities,name):
        self.probabilities = probabilities #stores the probabilities of each restaurant
        self.name = name #stores the name of the strategy used
        self.count = numpy.zeros(num_of_restaurants)#generates an array with the size proportionate to num of restaurants, with each value = 0
        self.reward_total = numpy.zeros(num_of_restaurants)#generates an array with size proportionate to num of restaurants, with each value = 0
        self.daily_rewards = numpy.zeros(num_of_days) #track the every day rewards which will be used to plot a graph
        self.best = 0 #current best value which is used in the exploit_only strategy
        self.epsilon = 0.1 #probability of exploring, i.e 10% of the time we should be exploring used for epsilon greedy

    #Method to calculate if a choice is rewarding
    def rewarding(self,choice):
        low, high = self.probabilities[choice] #Lower and Upper bound of the probabilities in the index choice
        probability = numpy.random.uniform(low, high) #generate a probability using the lower and upper bound
        satisfaction_score = probability * 10 #how satisfied the customer was between 1 to 10
        return numpy.round(satisfaction_score) #rounding to keep it consistent with no floats


num_of_days = 20000
num_of_restaurants = 20
test = BanditProblem(num_of_days,num_of_restaurants)
testStrategy = BanditProblemStrategies(test.probabilities,"test")

class TestCase(unittest.TestCase):

    def test_probability_generation(self): #test to check if 20 probabilities are generated
        self.assertEqual(len(test.probabilities),20)

    def test_probability_generation_upper_lower(self): #check if the probabilities are within the correct ranges
        for low,high in test.probabilities:
            self.assertTrue(low >= 0)
            self.assertTrue(high <= 1)

    def test_best_possible_satisfaction(self): #check that the calculated best satisfaction probability is correct
        for i in range(num_of_restaurants):
            low,high = test.probabilities[i]
            self.assertTrue(test.best_satisfaction >= high)

    def test_rewarding(self): #test that the rewarding function outputs a score between 1 and 10
        for choice in range(num_of_restaurants):
            reward = testStrategy.rewarding(choice)
            self.assertTrue(1 <= reward <= 10)


if __name__ == '__main__':
    unittest.main()




