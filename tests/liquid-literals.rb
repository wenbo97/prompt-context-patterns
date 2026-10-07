require 'json'
require 'liquid'
fixtures = JSON.parse(File.read('tests/fixtures/liquid-literals.json', encoding: 'utf-8'))
fixtures.each do |fixture|
  actual = Liquid::Template.parse(fixture.fetch('protected'), error_mode: :strict).render!
  raise "Literal changed: #{fixture.fetch('name')}" unless actual == fixture.fetch('original')
end
puts "#{fixtures.length} Liquid literal roundtrips passed"
