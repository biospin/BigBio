package org.bigbio.hadoop;

import org.apache.hadoop.conf.*;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapred.JobConf;
import org.junit.Test;

public class WordCountDriverTest {

	  @Test
	  public void test() throws Exception {
		JobConf conf = new JobConf();
		conf.set("fs.default.name", "file:///");
		conf.set("mapred.job.tracker", "local");
		//conf.set("hadoop.tmp.dir", "d:/tmp");
		
		Path input = new Path("input/README.txt");
		Path output = new Path("output");
		
		FileSystem fs = FileSystem.getLocal(conf);
		fs.delete(output, true); // delete old output
		
		WordCount driver = new WordCount();
		driver.setConf(conf);
		
		int exitCode = driver.run(new String[] {
	    	input.toString(), output.toString() });
		//assertThat(exitCode, is(0));
		
	  }
	
}
