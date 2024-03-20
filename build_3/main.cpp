#define PROFILE

#include "openfhe.h"

#include "ciphertext-ser.h"
#include "cryptocontext-ser.h"
#include "key/key-ser.h"
#include "scheme/bfvrns/bfvrns-ser.h"
#include <string>
using namespace lbcrypto;
using namespace std;

const std::string DATAFOLDER = "../build";

int main(int argc, char* argv[]) {
    CryptoContext<DCRTPoly> cc;
    if (!Serial::DeserializeFromFile(DATAFOLDER + "/cryptocontext.txt", cc, SerType::BINARY)) {
        std::cerr << "I cannot read serialization from " << DATAFOLDER + "/cryptocontext.txt" << std::endl;
        return 1;
    }
    std::cout << "The cryptocontext has been deserialized." << std::endl;

    PrivateKey<DCRTPoly> sk;
    if (Serial::DeserializeFromFile(DATAFOLDER + "/key-private.txt", sk, SerType::BINARY) == false) {
        std::cerr << "Could not read secret key" << std::endl;
        return 1;
    }
    std::cout << "The secret key has been deserialized." << std::endl;

    Ciphertext<DCRTPoly> ct2;
    if (Serial::DeserializeFromFile("./ciphertextAdd12.txt", ct2, SerType::BINARY) == false) {
        std::cerr << "Could not read the ciphertext" << std::endl;
        return 1;
    }
    std::cout << "The answer ciphertext has been deserialized." << std::endl;

    Plaintext plaintextAddResult;
    cc->Decrypt(sk, ct2, &plaintextAddResult);

    // std::cout << plaintextAddResult->Decode() << std::endl;
    std::cout << plaintextAddResult << std::endl;
    return 0;
}