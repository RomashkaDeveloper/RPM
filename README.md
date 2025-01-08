# RPM

### Installation

To start chatting with models you need to install using libraries

*Installing llama-cpp-python*
To install llama-cpp-python run this command

```bash
pip install llama-cpp-python
```

If it throws an error, you can do the following:

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp

mkdir build
cd build
cmake .. -G "Visual Studio 16 2019"  # Or use your version of Visual Studio
cmake --build . --config Release

pip install llama-cpp-python --no-binary llama-cpp-python
```

Don't forget to install cmake first from the official site!

Then install other libraries by yourself

### Usage

Run app.py and choose your dependencies to set up

Then run chat-v1.py 

