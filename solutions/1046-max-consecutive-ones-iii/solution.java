class Solution {
    public int longestOnes(int[] nums, int k) {
        int count = 0;
        int slow = 0;
        for(int i =0; i<nums.length;i++)
        {
            if(nums[i]==0)
            {
                count++;
            }
            if(count>k)
            {
                if(nums[slow]==0)
                {
                    count--;
                }
                slow++;
            }
        } 
        return nums.length-slow;
}
}
