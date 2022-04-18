import random
import datetime

geneSet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ! .,"
target="Hello, World!"

def gen_parent(length):
	genes=[]
	while len(genes)<length:
		sampleSize=min(length-len(genes),len(geneSet))
		genes.extend(random.sample(geneSet,sampleSize))
	return ''.join(genes)

def get_fitness(guess):
	return sum(1 for expected,actual in zip(target,guess) if expected==actual)

def mutate(parent):
	index=random.randrange(0,len(parent))
	childGenes=list(parent)
	newGene,alternate=random.sample(geneSet,2)
	childGenes[index]=alternate if newGene==childGenes[index] else newGene
	return ''.join(childGenes)

def display(guess):
	timeDiff=datetime.datetime.now()-startTime
	fitness=get_fitness(guess)
	print("{}\t{}\t{}".format(guess,fitness,timeDiff))

random.seed()
startTime=datetime.datetime.now()
print(f"startTime: {startTime}")
bestParent=gen_parent(len(target))
print(f"bestParent: {bestParent}")
bestFitness=get_fitness(bestParent)
print(f"bestFitness: {bestFitness}")
display(bestParent)

while True:
	child=mutate(bestParent)
	childFitness=get_fitness(child)
	if bestFitness>=childFitness:
		continue
	display(child)
	if childFitness==len(bestParent):
		break
	bestFitness=childFitness
	bestParent=child

# list1 = [1,2,3,4,5]
# list2 = [6,7,8,9,10]
# zipVal = list(zip(list1,list2))
# print(type(zipVal[1]))

# print('H'.isalpha() & 'H'.isupper())

