import tests.fixture_module.source as source
import tests.fixture_module.transformation as transformation
import tests.fixture_module.sink as sink


#@chains:task:name:test_orchestration
#@chains:task:compute:cpu:4
#@chains:task:ram:memory:8GB
#@chains:task:cron:"0 8 * * *"
def main():
    ds1 = source.get_data()
    transformed = transformation.transform_data(ds1)
    sink.write_data(transformed)

if __name__ == '__main__':
    main()
