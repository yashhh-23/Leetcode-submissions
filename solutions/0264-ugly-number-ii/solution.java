class Solution{
    public int nthUglyNumber(int n)
    {
        HashSet<Long> set = new HashSet<>();
        PriorityQueue<Long> pq = new PriorityQueue<>();
        pq.add(1l);
        set.add(1l);
        int count =0;
        long curr=0;
        int [] primes = new int []{2,3,5};
        while(count!=n)
        {
            curr=pq.poll();
            count++;
            for(int prime:primes)
            {
                long newUgly=prime*curr;
                if(!set.contains(newUgly))
                {
                    set.add(newUgly);
                    pq.add(newUgly);
                }
            }
        }
        return (int)curr;
    }
}
