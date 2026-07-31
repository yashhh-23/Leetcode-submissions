class Solution {
    List<List<String>> result;
    public List<List<String>> partition(String s) {
        this.result = new ArrayList<>();
        helper(s, new ArrayList<>());
        return result;
    }

    private void helper(String s, List<String> path){
        if(s.length() == 0){
            result.add(new ArrayList<>(path));
            return; 
        }
        for(int i=0; i<s.length(); i++){
            String subStr = s.substring(0, i+1);
            if(isPalindrome(subStr)){
                //action
                path.add(subStr);
                //recurse
                helper(s.substring(i+1), path);
                //backtrack
                path.remove(path.size()-1);
            }
        }
    }

    private boolean isPalindrome(String s){
        int left = 0, right = s.length()-1;
        while(left < right){
            if(s.charAt(left) != s.charAt(right))
                return false;
            left++; 
            right--;
        }
        return true;
    }
}

