#define PROFILE

#include "openfhe.h"

#include "ciphertext-ser.h"
#include "cryptocontext-ser.h"
#include "key/key-ser.h"
#include "scheme/bfvrns/bfvrns-ser.h"
#include <string>
using namespace lbcrypto;
using namespace std;


int main(int argc, char* argv[]) {
    cout << argv[1] << endl;
    cout << argv[2] << endl;

    CCParams<CryptoContextBFVRNS> parameters;
    parameters.SetPlaintextModulus(65537);
    parameters.SetMultiplicativeDepth(2);

    CryptoContext<DCRTPoly> cryptoContext = GenCryptoContext(parameters);
    cryptoContext->Enable(PKE);
    cryptoContext->Enable(KEYSWITCH);
    cryptoContext->Enable(LEVELEDSHE);

    if (!Serial::SerializeToFile("cryptocontext.txt", cryptoContext, SerType::BINARY)) {
        std::cerr << "Error writing serialization of the crypto context to "
                     "cryptocontext.txt"
                  << std::endl;
        return 1;
    }

    KeyPair<DCRTPoly> keyPair;

    keyPair = cryptoContext->KeyGen();

    Serial::SerializeToFile("key-public.txt", keyPair.publicKey, SerType::BINARY);

    Serial::SerializeToFile("key-private.txt", keyPair.secretKey, SerType::BINARY);

    cryptoContext->EvalMultKeyGen(keyPair.secretKey);

    std::ofstream emkeyfile("key-eval-mult.txt", std::ios::out | std::ios::binary);
    if (emkeyfile.is_open()) {
        if (cryptoContext->SerializeEvalMultKey(emkeyfile, SerType::BINARY) == false) {
            std::cerr << "Error writing serialization of the eval mult keys to "
                         "key-eval-mult.txt"
                      << std::endl;
            return 1;
        }
        std::cout << "The eval mult keys have been serialized." << std::endl;

        emkeyfile.close();
    }
    else {
        std::cerr << "Error serializing eval mult keys" << std::endl;
        return 1;
    }

    cryptoContext->EvalRotateKeyGen(keyPair.secretKey, {1, 2, -1, -2});

    std::ofstream erkeyfile("key-eval-rot.txt", std::ios::out | std::ios::binary);
    if (erkeyfile.is_open()) {
        if (cryptoContext->SerializeEvalAutomorphismKey(erkeyfile, SerType::BINARY) == false) {
            std::cerr << "Error writing serialization of the eval rotation keys to "
                         "key-eval-rot.txt"
                      << std::endl;
            return 1;
        }
        std::cout << "The eval rotation keys have been serialized." << std::endl;

        erkeyfile.close();
    }
    else {
        std::cerr << "Error serializing eval rotation keys" << std::endl;
        return 1;
    }

    std::vector<int64_t> vectorOfInts1 = {stoi(argv[1])};
    Plaintext plaintext1 = cryptoContext->MakePackedPlaintext(vectorOfInts1);

    std::vector<int64_t> vectorOfInts2 = {stoi(argv[2])};
    Plaintext plaintext2 = cryptoContext->MakePackedPlaintext(vectorOfInts2);

    auto ciphertext1 = cryptoContext->Encrypt(keyPair.publicKey, plaintext1);
    auto ciphertext2 = cryptoContext->Encrypt(keyPair.publicKey, plaintext2);

    Serial::SerializeToFile("ciphertext1.txt", ciphertext1, SerType::BINARY);
    Serial::SerializeToFile("ciphertext2.txt", ciphertext2, SerType::BINARY);
    return 0;
}

/*
cryptocontext.txt
key-public.txt
key-eval-mult.txt
key-eval-rot.txt
ciphertext1.txt
ciphertext2.txt
*/