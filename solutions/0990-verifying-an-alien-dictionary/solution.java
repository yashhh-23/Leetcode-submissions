class Solution {
    HashMap<Character, Integer> map;
    public boolean isAlienSorted(String[] words, String order) {
        this.map = new HashMap<>();
        for(int i=0; i<order.length(); i++){
            char c = order.charAt(i);
            map.put(c, i);
        }

        for(int i=0; i<words.length-1; i++){
            String first = words[i];
            String second = words[i+1];

            if(notSorted(first, second)) return false;
        }

        return true;
    }

    private boolean notSorted(String first, String second){

        for(int i=0; i<first.length() && i < second.length(); i++){
            char fChar = first.charAt(i);
            char sChar = second.charAt(i);

            if(fChar != sChar){
                return map.get(fChar) > map.get(sChar);  // apple, app
            }
        }

        return first.length() > second.length();
    }
}

