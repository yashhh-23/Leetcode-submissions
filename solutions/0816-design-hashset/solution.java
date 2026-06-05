class MyHashSet {
    private boolean[][] storage;
    private int buckets;
    private int bucketItems;

    public MyHashSet() {
        this.buckets = 1000;
        this.bucketItems = 1001;
        this.storage = new boolean[buckets][];
    }

    private int hash(int key) {
        return key % buckets;
    }

    private int pos(int key) {
        return key / buckets;
    }

    public void add(int key) {
        int bucket = hash(key);
        int bucketItem = pos(key);

        if (storage[bucket] == null) {
            storage[bucket] = new boolean[bucketItems];
        }
        storage[bucket][bucketItem] = true;
    }

    public void remove(int key) {
        int bucket = hash(key);
        int bucketItem = pos(key);

        if (storage[bucket] != null) {
            storage[bucket][bucketItem] = false;
        }
    }

    public boolean contains(int key) {
        int bucket = hash(key);
        int bucketItem = pos(key);

        return storage[bucket] != null && storage[bucket][bucketItem];
    }
}
