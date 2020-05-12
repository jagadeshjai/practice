namespace CountSeqQues
{
    class Program
    {
        static void Main(string[] args)
        {
           
            PrintSequence obj = new PrintSequence();
            System.Console.WriteLine("Enter the sentence");
            string sentence = System.Convert.ToString(System.Console.ReadLine());
            int length = sentence.Length;
            System.Console.WriteLine("Enter the number");
            int number = System.Convert.ToInt32(System.Console.ReadLine());

            System.Console.WriteLine(obj.Printing(sentence,length,number));
        }
    }

     
    public class PrintSequence
    {
        public string Printing(string sentence,int length,int number)
        {
            string res = "";
            length = sentence.Length;
            if(number>0 && number<10)
            {
                if (length<3)
                {
                    System.Console.WriteLine("Input value is insufficient");
                }
                else if(length<=5)
                {
                    res = sentence.Substring(0, 3);
                    for(int i=0;i<number;i=i+res.Length)
                    {
                        int k = number - 1;
                        if (k > res.Length)
                            k = res.Length;
                        for(int j=0;j<k;j++)
                        {
                            System.Console.Write(res[j]);
                        }
                    }
                }
                else if (length > 5)
                {
                    res = sentence.Substring(length-3);
                    for (int i = 0; i < number; i = i + res.Length)
                    {
                        int k = number - 1;
                        if (k > res.Length)
                            k = res.Length;
                        for (int j = 0; j < k; j++)
                        {
                            System.Console.Write(res[j]);
                        }
                    }
                }
            }
            else if (number<0)
            {
                System.Console.WriteLine("Invalid Input");
            }
            else if (number>10)
            {
                System.Console.WriteLine("Too long");
            }
            return res;
        }
    }

}