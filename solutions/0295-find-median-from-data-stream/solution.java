class MedianFinder {
        private PriorityQueue<Integer> maxheap;
        private PriorityQueue<Integer> minheap;
    public MedianFinder() {
        maxheap= new PriorityQueue<>(Collections.reverseOrder());
        minheap= new PriorityQueue<>();
    }
    
    public void addNum(int num) {
        maxheap.offer(num);
        minheap.offer(maxheap.poll());
        if(maxheap.size()<minheap.size())
        {
            maxheap.offer(minheap.poll());
        }
    }
    
    public double findMedian() {
        if(maxheap.size()>minheap.size())
        {
            return (double) maxheap.peek();
        } else
        {
            return (maxheap.peek() + (double) minheap.peek())/2.0;
        }
        
    }
}

/**
 * Your MedianFinder object will be instantiated and called as such:
 * MedianFinder obj = new MedianFinder();
 * obj.addNum(num);
 * double param_2 = obj.findMedian();
 */
