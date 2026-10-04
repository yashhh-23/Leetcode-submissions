class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        if(nums==null||nums.length==0) return result;
        backtrack(0, nums, result);
        return result;
    } private void backtrack(int start, int [] nums, List<List<Integer>> result)
    {
        if(start==nums.length)
        {
            List<Integer> permutation = new ArrayList<>(nums.length);
            for(int num:nums)
            {
                permutation.add(num);
            } 
            result.add(permutation);
            return;
        } 
        for(int i = start; i< nums.length;i++){
            swap(nums, start, i);
            backtrack(start+1, nums, result);
            swap(nums,start,i);
        }
    } private void swap(int [] nums, int i, int j)
    {
        int temp =  nums[i];
        nums[i]= nums[j];
        nums[j]=temp;
    }
}
