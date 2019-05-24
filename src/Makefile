
output: blockchain.o sha256.o
	g++ blockchain.o sha256.o -o output

blockchain.o: blockchain.cpp blockchain.h
	g++ -c blockchain.cpp

sha2.o: sha256.cpp sha256.h
	g++ -c sha256.cpp

clean: 
	rm *.o output

# run `make` to compile
# run `./output` to run program
# run `make clean` to clear all compiled files