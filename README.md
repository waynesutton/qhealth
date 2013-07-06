# QHealth
Create Personal Quantified Health Profiles to share with the world.

## Notes to developers
You can run this app your local machine as follows:

    $ cd /tmp
	$ git clone https://github.com/waynesutton/qhealth
	$ cd qhealth
	$ bundle install
	$ bundle exec rake db:migrate
	$ bundle exec rake db:test:prepare
	$ bundle exec rspec spec/

To add a remote git:

	$ git remote add canon https://github.com/waynesutton/qhealth

Then create a new branch

	$ git checkout canon/master -b your_branch_name

When you are ready to push it, you can do
	
	$ git push canon HEAD

Then ask me (Tum) to merge it to the master branch.

## Credits
The version 0.0.1 of this app is based on the sample application for [*Ruby on Rails Tutorial: Learn Rails by Example*](http://railstutorial.org/) by [Michael Hartl](http://michaelhartl.com/).