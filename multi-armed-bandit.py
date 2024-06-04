import numpy
import matplotlib.pyplot as plt 

#create a very basic multi-armed bandit problem
numpy.set_printoptions(suppress=True) # set print options to not do scientific mode
#A man going to eat at a restaurant everyday for a year
num_of_days = 20000 #increase for a larger sample size - how many days he visits a restaurant
num_of_restaurants = 20 #random number of restaurants

#Class to create a Bandit Problem using an OOP approach
class BanditProblem:
    def __init__(self,num_of_days,num_of_restaurants):
        self.num_of_days = num_of_days #how many days we visit each restaurant
        self.num_of_restaurants = num_of_restaurants #how many restaurant options there are
        self.probabilities = self.generate_probabilities() #variable storing the range of probabilities
        self.best_expected_satisfaction = self.best_possible_expected_satisfaction() #the best possible value from the range of distributions if you picked the most optimal choice

    #Method to generate the probabilities for each restaurant
    def generate_probabilities(self):
        ranges = [] #creates an array
        for i in range (self.num_of_restaurants): #iterates for how many restaurants there are
            low = numpy.random.uniform(0,0.7) #generates a random number between 0 and 1 for lower bound
            high = numpy.random.uniform(low,1) #use uniform to make sure upper bound is larger than the lower bound
            ranges.append((low,high))#into the array append the the range of potential satisfaction
        return ranges #returns the array
    
    def best_possible_expected_satisfaction(self):
        expected_satisfactions = []
        for low, high in self.probabilities:
            average_probability = (low + high) / 2 
            expected_satisfaction = numpy.round(average_probability * 10)
            expected_satisfactions.append(expected_satisfaction)
        best_expected = max(expected_satisfactions) * self.num_of_days
        return best_expected


#Class that stores the strategies used to solve the bandit problem
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

    def statistics_updater(self,choice,reward,day):
        self.count[choice] = self.count[choice] + 1 #in the array of zeros we created, positions 0 to the number of restaurants,it will increment the visited restaurant by 1 using index choice
        self.reward_total[choice] = self.reward_total[choice] + reward #in the array of zeroes created, using the index choice, it will add the satisfaction_score from that restaurant
        self.daily_rewards[day] = self.daily_rewards[day] + reward #add the reward for the day

    #Strategy to randomly select a restaurant
    def random_probability(self,day):
        choice = numpy.random.choice(num_of_restaurants)#generates a number from 0 to the number of restaurants
        reward = self.rewarding(choice)#using the index choice, we use the method rewarding to calculate the reward
        self.statistics_updater(choice,reward,day) #calls the method statistics_updater to update the attribute values

    #Strategy to explore each restaurant evenly
    def explore_only(self,day):
        #we need to select a restaurant
        choice = day % num_of_restaurants #using mod to make it visit each option evenly
        reward = self.rewarding(choice)#using the index choice, we use the method rewarding to calculate the reward
        self.statistics_updater(choice,reward,day) #calls the method statistics_updater to update the attribute values

    #Strategy that visits each restaurant once and exploits the best option
    def exploit_only(self,day):
        if numpy.sum(self.count) < num_of_restaurants: #check if each restaurant has been visited once
            choice = day #selecting the option based on the day
        else:
            choice = self.best #gets the best option from the 5 restaurants from the initial visit

        reward = self.rewarding(choice) #using the index choice, we use the method rewarding to calculate the reward
        self.statistics_updater(choice,reward,day)
        if day == num_of_restaurants - 1: #once the last restaurant is visited
            self.best = numpy.argmax(self.reward_total) # argmax gets the index of the largest value in the array aka the best value out of the initial restaurants which will be used for the rest of the program

    #Method to generate the UCB values 
    def UCB1_VALUES(self):
        UCB_VALUE_ARRAY = numpy.zeros(num_of_restaurants)#Creates an array of zeros for the number of restaurants
        for i in range(num_of_restaurants):#iterates through every restaurant
            #calculate the UCB value using the UCB1 formula which is mean + exploration term
            mean = self.reward_total[i] / self.count[i] #calculate the mean using the total satisfasction of the restaurant divided by how many times the restaurant has been visited
            exploration_term = numpy.sqrt(2 * numpy.log(numpy.sum(self.count)) / self.count[i]) #to calculate it, its just the square root of 2*ln*N / n, where N = total visits to each restaurant and n = the amount of visits for the selected restaurant
            UCB_VALUE_ARRAY[i] = mean + exploration_term #at value i in the array, append the UCB value
        return numpy.argmax(UCB_VALUE_ARRAY)#returns the index of the largest UCB value
    
    #Strategy that picks the highest UCB value
    def UCB1(self,day):
        #for the first 5 days, we want to visit each restaurant once, this is to make it so that we do not divide by 0
        if numpy.sum(self.count) < num_of_restaurants: #check if each restaurant has been visited once
            choice = day
        else:
            choice = self.UCB1_VALUES()#get the index of the largest UCB Value

        reward = self.rewarding(choice)#using the index choice, we use the method rewarding to calculate the reward
        self.statistics_updater(choice,reward,day) #calls the method statistics_updater to update the attribute values

    #Strategy that explores and exploits based on a predefined value
    def epsilon_greedy(self,day):
        #first 5 days, we visit each restaurant once, this is to avoid dividing by 0
        if numpy.sum(self.count) < num_of_restaurants: #check if each restaurant has been visited once
            choice = day
        else:
            if numpy.random.rand() <= self.epsilon: #at the start of each day, we generate a number between 0 and 1, if the number is less than or equal to the epsilon value, we explore
                choice = numpy.random.choice(num_of_restaurants) #this selects a number between 0 and the number of restaurants
            else:
                #we need to choose the best option out of the restaurants, to do this we final the averages of all the rewards and pick the highest number
                reward_average = self.reward_total / self.count #dividing the two arrays gets the average reward of each restaurant
                choice = numpy.argmax(reward_average)#returns the index of the largest value in the array

        reward = self.rewarding(choice)#using the index choice, we use the method rewarding to calculate the reward
        self.statistics_updater(choice,reward,day)

BanditProblem = BanditProblem(num_of_days,num_of_restaurants) #create the bandit problem object

random_probability = BanditProblemStrategies(BanditProblem.probabilities,"random_probability") #random_probability object
explore_only = BanditProblemStrategies(BanditProblem.probabilities,"explore_only") #explore_only object
exploit_only = BanditProblemStrategies(BanditProblem.probabilities,"exploit_only") #exploit_only object
UCB1 = BanditProblemStrategies(BanditProblem.probabilities, "UCB1") #UCB1 object
epsilon_greedy = BanditProblemStrategies(BanditProblem.probabilities, "epsilon_greedy") #epsilon_greedy object

list = [random_probability,explore_only,exploit_only,UCB1, epsilon_greedy] #put them in a list to plot on the graph

#To calculate each day we will use a for loop
for day in range(num_of_days):
    random_probability.random_probability(day) #test the random strategy every day
    explore_only.explore_only(day) #test the explore_only strategy every day
    exploit_only.exploit_only(day) #test the exploit_only strategy every day
    UCB1.UCB1(day) #test the UCB1 strategy everyday
    epsilon_greedy.epsilon_greedy(day) #test the epsilon_greedy strategy everyday


plt.figure(figsize=(14, 7)) #create a new figure to plot 14 inches width, 7 inches height
days = numpy.arange(1, num_of_days + 1) #generate an array with values from 1 to num_of_days


for solution in list:
    #next we need to print the values of the results to see that it is working
    print("For {}:".format(solution.name)) #name of the strategy
    print("Maximum satisfaction possible: ", BanditProblem.best_expected_satisfaction) #total possible satisfaction
    print("Satisfaction total: ", numpy.sum(solution.reward_total))#since reward_total is an array, numpy.sum is to add all the values in the array together to give sum satisfaction of strategy
    print("Regret: ", BanditProblem.best_expected_satisfaction - numpy.sum(solution.reward_total)) # max - total = regret which is how much is left over
    print("Each time a restaurant was chosen: ", solution.count) #print the array for how much each restaurant was chosen
    print("Satisfaction of each restaurant: ", solution.reward_total)#prints how satisfying each restaurant is
    print("Probabilities of a satisfying meal", BanditProblem.probabilities)#print the array of probabilities for each restaurant
    print("                      ")#space

    cumulative_regret = numpy.cumsum((BanditProblem.best_expected_satisfaction / num_of_days) - solution.daily_rewards)
    
    # Plotting on a logarithmic scale
    plt.semilogy(days, cumulative_regret, label=solution.name)


plt.title('UCB vs Naive Strategies against multi-armed Bandit problem') #title for the plot
plt.xlabel('Day') #label for x value
plt.ylabel('Regret Over Time') #label for y value
plt.legend() #displays on top left what coloured line is what method
plt.grid(True) #adds a grid to the plot
plt.show() #renders the plot