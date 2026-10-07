require 'jekyll'
require 'tmpdir'
require 'rexml/document'
require 'json'

root = File.expand_path('..', __dir__)
patterns = JSON.parse(File.read(File.join(root, '_data/patterns.json'), encoding: 'utf-8'))
active_paths = patterns.select { |row| row['status'] == 'active' }.flat_map do |row|
  ["/catalog/patterns/#{row['id']}/", "/catalog/patterns/#{row['id']}-zh/"]
end

Dir.mktmpdir('pattern-sitemap-dates-') do |directory|
  results = ['2001-01-01 12:00:00 +0000', '2002-02-02 12:00:00 +0000'].each_with_index.map do |time, index|
    config = Jekyll.configuration('source' => root, 'destination' => File.join(directory, index.to_s),
                                  'time' => time, 'quiet' => true, 'future' => true)
    Jekyll::Site.new(config).process
    xml = REXML::Document.new(File.read(File.join(config['destination'], 'sitemap.xml')))
    entries = {}
    REXML::XPath.each(xml, '//url') do |entry|
      url = entry.elements['loc'].text
      relative = URI(url).path.delete_prefix(config['baseurl'])
      next unless active_paths.include?(relative)
      entries[relative] = entry.elements['lastmod']&.text
    end
    raise "Missing content dates: #{entries.size}/#{active_paths.size}" unless entries.size == active_paths.size && entries.values.none?(&:nil?)
    entries
  end
  raise 'Pattern lastmod changed with build time' unless results[0] == results[1]
  puts "#{active_paths.size} authored sitemap dates remain stable across different build times"
end
