
import configparser
while True:
    print('Choose your method:\n1.transormers\2.unsloth')
    user_method_id = input('—> ')

    if user_metbreakhod_is == 1:
        print('choose your model\n1.gg\n2.hh\3.kk\n4. custom model')
        user_model_id = input('—> ')
        if user_model_id == 1:
            model = ""
        elif user_model_id == 2:
            model = ""
        elif user_model_id == 3:
            model = ""
        else:
            model = input('Type your model’s name here: ')
        method = "transformers"
        break
    elif user_method_is == 2:
        print('choose your model\n1.gg\n2.hh\n3.ll\n4. custom model')
        user_model_id = input('—> ')
        if user_model_id == 1:
            model = ""
        elif user_model_id == 2:
            model = ""
        elif user_model_id == 3:
            model = ""
        else:
            model = input('Type your model’s name here: ')
        method = "unsloth"
        break
    else:
        print('ты дегенерат')
config = configparser.ConfigParser()
config['SYSTEM']['model'] = model
config['SYSTEM']['method'] = method
with open('config.ini', 'w') as configfile:
    config.write(configfile)
