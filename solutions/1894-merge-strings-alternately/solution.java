	public class Solution {

	    public String mergeAlternately(String word1, String word2) {

	        int A = word1.length(), B = word2.length();

	        int a = 0, b = 0;

	        StringBuilder s = new StringBuilder();

	 

	        int word = 1;

	        while (a < A && b < B) {

	            if (word == 1) {

	                s.append(word1.charAt(a++));

	                word = 2;

	            } else {

	                s.append(word2.charAt(b++));

	                word = 1;

	            }

	        }

	 

	        while (a < A) {

	            s.append(word1.charAt(a++));

	        }

	 

	        while (b < B) {

	            s.append(word2.charAt(b++));

	        }

	 

	        return s.toString();

	    }

	}
