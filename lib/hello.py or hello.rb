#!python-or-ruby
# https://nkanaev.com/posts/polyglot/

print(0 and eval("""

3.times do
  puts 'Hello from Ruby'
end

""") or exec("""

for i in range(3):
  print('Hello from Python')

"""))
