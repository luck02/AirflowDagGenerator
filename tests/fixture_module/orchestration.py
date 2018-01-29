import tests.fixture_module.source as source
import tests.fixture_module.transformation as transformation
import tests.fixture_module.sink as sink



def main():
    ds1 = source.get_data()
    transformed = transformation.transform_data(ds1)
    sink.write_data(transformed)

if __name__ == '__main__':
    main()
